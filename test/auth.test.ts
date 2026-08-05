import assert from 'node:assert/strict';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import { after, before, beforeEach, describe, it } from 'node:test';
import { createApp } from '../src/app.js';
import { loadConfig, type Config } from '../src/config.js';
import { openDatabase, type Database } from '../src/db.js';
import { revokeAllSessionsForUser } from '../src/sessions.js';

const CREDENTIALS = { email: 'ada@example.com', password: 'correct-horse-battery' };

let db: Database;
let config: Config;
let server: Server;
let baseUrl: string;

interface TokenPair {
  accessToken: string;
  refreshToken: string;
  sessionId: string;
}

async function call(
  method: string,
  path: string,
  options: { token?: string; body?: unknown; deviceLabel?: string } = {},
): Promise<{ status: number; body: any }> {
  const headers: Record<string, string> = { 'content-type': 'application/json' };
  if (options.token) headers.authorization = `Bearer ${options.token}`;
  if (options.deviceLabel) headers['user-agent'] = options.deviceLabel;

  const init: RequestInit = { method, headers };
  if (options.body !== undefined) init.body = JSON.stringify(options.body);

  const response = await fetch(`${baseUrl}${path}`, init);
  return { status: response.status, body: await response.json() };
}

/** Signs in as the same user again, simulating a new device. */
async function signInFrom(deviceLabel: string): Promise<TokenPair> {
  const { status, body } = await call('POST', '/auth/login', {
    body: { ...CREDENTIALS, deviceLabel },
    deviceLabel,
  });
  assert.equal(status, 200, `login from ${deviceLabel} failed: ${JSON.stringify(body)}`);
  return body as TokenPair;
}

before(async () => {
  config = loadConfig({ AUTH_JWT_SECRET: 'test-secret', SESSION_TOUCH_INTERVAL: '1' });
  db = openDatabase(':memory:');
  server = createApp({ db, config }).listen(0);
  await new Promise<void>((resolve) => server.once('listening', resolve));
  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

after(() => {
  server.close();
  db.close();
});

beforeEach(() => {
  db.exec('DELETE FROM sessions');
  db.exec('DELETE FROM users');
});

async function register(): Promise<TokenPair> {
  const { status, body } = await call('POST', '/auth/register', { body: CREDENTIALS });
  assert.equal(status, 201, `register failed: ${JSON.stringify(body)}`);
  return body as TokenPair;
}

describe('logging out of all devices', () => {
  it('revokes every session, including the one that made the request', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');
    const tablet = await signInFrom('tablet');

    // All three devices work beforehand.
    for (const device of [laptop, phone, tablet]) {
      assert.equal((await call('GET', '/auth/sessions', { token: device.accessToken })).status, 200);
    }

    const result = await call('POST', '/auth/logout-all', { token: laptop.accessToken, body: {} });
    assert.equal(result.status, 200);
    assert.equal(result.body.revokedCount, 3);
    assert.equal(result.body.keptCurrent, false);

    // Every device is signed out at once, without waiting for token expiry.
    for (const device of [laptop, phone, tablet]) {
      const check = await call('GET', '/auth/sessions', { token: device.accessToken });
      assert.equal(check.status, 401);
      assert.equal(check.body.error, 'session_revoked');
    }
  });

  it('takes effect immediately, not when the access token expires', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');

    // The phone's access token is still cryptographically valid and unexpired...
    const claims = JSON.parse(
      Buffer.from(phone.accessToken.split('.')[1]!, 'base64url').toString('utf8'),
    );
    assert.ok(claims.exp * 1000 > Date.now(), 'precondition: token has not expired');

    await call('POST', '/auth/logout-all', { token: laptop.accessToken, body: {} });

    // ...yet it is rejected, because the session behind it is gone.
    const check = await call('GET', '/auth/sessions', { token: phone.accessToken });
    assert.equal(check.status, 401);
  });

  it('can keep the current device signed in', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');
    const tablet = await signInFrom('tablet');

    const result = await call('POST', '/auth/logout-all', {
      token: laptop.accessToken,
      body: { keepCurrent: true },
    });
    assert.equal(result.status, 200);
    assert.equal(result.body.revokedCount, 2);
    assert.equal(result.body.keptCurrent, true);

    const remaining = await call('GET', '/auth/sessions', { token: laptop.accessToken });
    assert.equal(remaining.status, 200);
    assert.equal(remaining.body.sessions.length, 1);
    assert.equal(remaining.body.sessions[0].current, true);

    for (const device of [phone, tablet]) {
      assert.equal((await call('GET', '/auth/sessions', { token: device.accessToken })).status, 401);
    }
  });

  it('stops revoked devices from refreshing their way back in', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');

    await call('POST', '/auth/logout-all', { token: laptop.accessToken, body: {} });

    const refreshed = await call('POST', '/auth/refresh', {
      body: { refreshToken: phone.refreshToken },
    });
    assert.equal(refreshed.status, 401);
  });

  it('is idempotent — a second call revokes nothing more', async () => {
    const laptop = await register();
    await signInFrom('phone');

    const first = await call('POST', '/auth/logout-all', {
      token: laptop.accessToken,
      body: { keepCurrent: true },
    });
    assert.equal(first.body.revokedCount, 1);

    const second = await call('POST', '/auth/logout-all', {
      token: laptop.accessToken,
      body: { keepCurrent: true },
    });
    assert.equal(second.body.revokedCount, 0);
  });

  it('does not touch other users', async () => {
    const laptop = await register();
    await call('POST', '/auth/register', {
      body: { email: 'grace@example.com', password: 'a-different-password' },
    });
    const other = await call('POST', '/auth/login', {
      body: { email: 'grace@example.com', password: 'a-different-password' },
    });

    await call('POST', '/auth/logout-all', { token: laptop.accessToken, body: {} });

    const check = await call('GET', '/auth/sessions', { token: other.body.accessToken });
    assert.equal(check.status, 200);
  });
});

describe('listing and revoking individual devices', () => {
  it('lists active sessions and marks the current one', async () => {
    const laptop = await register();
    await signInFrom('phone');

    const { status, body } = await call('GET', '/auth/sessions', { token: laptop.accessToken });
    assert.equal(status, 200);
    assert.equal(body.sessions.length, 2);
    assert.equal(body.sessions.filter((s: { current: boolean }) => s.current).length, 1);
    assert.ok(!('refreshTokenHash' in body.sessions[0]), 'must not leak token material');
  });

  it('revokes a single named device', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');

    const result = await call('DELETE', `/auth/sessions/${phone.sessionId}`, {
      token: laptop.accessToken,
    });
    assert.equal(result.status, 200);
    assert.equal(result.body.revokedCount, 1);

    assert.equal((await call('GET', '/auth/sessions', { token: phone.accessToken })).status, 401);
    assert.equal((await call('GET', '/auth/sessions', { token: laptop.accessToken })).status, 200);
  });

  it("will not let one user revoke another user's session", async () => {
    const laptop = await register();
    await call('POST', '/auth/register', {
      body: { email: 'grace@example.com', password: 'a-different-password' },
    });
    const other = await call('POST', '/auth/login', {
      body: { email: 'grace@example.com', password: 'a-different-password' },
    });

    const result = await call('DELETE', `/auth/sessions/${other.body.sessionId}`, {
      token: laptop.accessToken,
    });
    assert.equal(result.status, 404);
    assert.equal((await call('GET', '/auth/sessions', { token: other.body.accessToken })).status, 200);
  });

  it('logout revokes only the calling device', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');

    assert.equal((await call('POST', '/auth/logout', { token: laptop.accessToken })).status, 200);
    assert.equal((await call('GET', '/auth/sessions', { token: laptop.accessToken })).status, 401);
    assert.equal((await call('GET', '/auth/sessions', { token: phone.accessToken })).status, 200);
  });
});

describe('refresh tokens', () => {
  it('rotates on use and rejects the old token', async () => {
    const laptop = await register();

    const first = await call('POST', '/auth/refresh', {
      body: { refreshToken: laptop.refreshToken },
    });
    assert.equal(first.status, 200);
    assert.notEqual(first.body.refreshToken, laptop.refreshToken);

    const replay = await call('POST', '/auth/refresh', {
      body: { refreshToken: laptop.refreshToken },
    });
    assert.equal(replay.status, 401);
  });

  it('treats reuse of a revoked session token as a breach and signs everything out', async () => {
    const laptop = await register();
    const phone = await signInFrom('phone');

    // The laptop signs itself out; its refresh token then leaks and is replayed.
    await call('POST', '/auth/logout', { token: laptop.accessToken });

    const replay = await call('POST', '/auth/refresh', {
      body: { refreshToken: laptop.refreshToken },
    });
    assert.equal(replay.status, 401);
    assert.equal(replay.body.error, 'refresh_token_reuse');

    // The still-innocent phone is signed out too — the safe response to a leak.
    assert.equal((await call('GET', '/auth/sessions', { token: phone.accessToken })).status, 401);
  });
});

describe('auth basics', () => {
  it('rejects duplicate registrations', async () => {
    await register();
    const again = await call('POST', '/auth/register', { body: CREDENTIALS });
    assert.equal(again.status, 409);
  });

  it('rejects bad credentials and weak passwords', async () => {
    await register();
    assert.equal(
      (await call('POST', '/auth/login', { body: { ...CREDENTIALS, password: 'wrong' } })).status,
      401,
    );
    assert.equal(
      (await call('POST', '/auth/register', { body: { email: 'x@example.com', password: 'short' } }))
        .status,
      400,
    );
  });

  it('rejects tampered and missing tokens', async () => {
    const laptop = await register();
    assert.equal((await call('GET', '/auth/sessions')).status, 401);
    assert.equal(
      (await call('GET', '/auth/sessions', { token: `${laptop.accessToken}x` })).status,
      401,
    );
  });
});

describe('revokeAllSessionsForUser', () => {
  it('reports how many sessions it ended', async () => {
    await register();
    await signInFrom('phone');
    await signInFrom('tablet');

    const userId = (db.prepare('SELECT id FROM users LIMIT 1').get() as { id: string }).id;
    assert.equal(revokeAllSessionsForUser(db, userId), 3);
    assert.equal(revokeAllSessionsForUser(db, userId), 0);
  });
});
