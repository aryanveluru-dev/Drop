import { Router, type Request, type Response } from 'express';
import type { Config } from './config.js';
import type { Database } from './db.js';
import { signAccessToken } from './crypto.js';
import { requireAuth } from './auth-middleware.js';
import {
  authenticate,
  createUser,
  EmailTakenError,
  findUserById,
  type UserRow,
} from './users.js';
import {
  createSession,
  findSessionById,
  findSessionByRefreshToken,
  isActive,
  listActiveSessions,
  revokeAllSessionsForUser,
  revokeSession,
  rotateRefreshToken,
  toPublicSession,
  type DeviceContext,
} from './sessions.js';

const MIN_PASSWORD_LENGTH = 8;
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function asString(value: unknown): string | null {
  return typeof value === 'string' && value.trim().length > 0 ? value.trim() : null;
}

function deviceContextFrom(req: Request): DeviceContext {
  const body = (req.body ?? {}) as Record<string, unknown>;
  return {
    deviceLabel: asString(body.deviceLabel),
    userAgent: req.get('user-agent') ?? null,
    ip: req.ip ?? null,
  };
}

function issueTokens(
  db: Database,
  config: Config,
  user: UserRow,
  device: DeviceContext,
): { accessToken: string; refreshToken: string; sessionId: string; expiresIn: number } {
  const { session, refreshToken } = createSession(
    db,
    user.id,
    config.refreshTokenTtlSeconds,
    device,
  );
  const accessToken = signAccessToken(
    { sub: user.id, sid: session.id },
    config.jwtSecret,
    config.accessTokenTtlSeconds,
  );
  return {
    accessToken,
    refreshToken,
    sessionId: session.id,
    expiresIn: config.accessTokenTtlSeconds,
  };
}

export function createRouter(db: Database, config: Config): Router {
  const router = Router();
  const auth = requireAuth(db, config);

  router.post('/auth/register', (req: Request, res: Response): void => {
    const body = (req.body ?? {}) as Record<string, unknown>;
    const email = asString(body.email);
    const password = typeof body.password === 'string' ? body.password : '';

    if (!email || !EMAIL_PATTERN.test(email)) {
      res.status(400).json({ error: 'invalid_email', message: 'A valid email is required' });
      return;
    }
    if (password.length < MIN_PASSWORD_LENGTH) {
      res.status(400).json({
        error: 'weak_password',
        message: `Password must be at least ${MIN_PASSWORD_LENGTH} characters`,
      });
      return;
    }

    let user: UserRow;
    try {
      user = createUser(db, email, password);
    } catch (error) {
      if (error instanceof EmailTakenError) {
        res.status(409).json({ error: 'email_taken', message: error.message });
        return;
      }
      throw error;
    }

    res.status(201).json({
      user: { id: user.id, email: user.email },
      ...issueTokens(db, config, user, deviceContextFrom(req)),
    });
  });

  router.post('/auth/login', (req: Request, res: Response): void => {
    const body = (req.body ?? {}) as Record<string, unknown>;
    const email = asString(body.email);
    const password = typeof body.password === 'string' ? body.password : '';

    const user = email ? authenticate(db, email, password) : null;
    if (!user) {
      res.status(401).json({ error: 'invalid_credentials', message: 'Email or password is incorrect' });
      return;
    }

    res.json({
      user: { id: user.id, email: user.email },
      ...issueTokens(db, config, user, deviceContextFrom(req)),
    });
  });

  /**
   * Rotates the refresh token on every use. Presenting a token that belongs to
   * an already-revoked session means the token leaked after that session ended,
   * so every session for the user is torn down.
   */
  router.post('/auth/refresh', (req: Request, res: Response): void => {
    const body = (req.body ?? {}) as Record<string, unknown>;
    const refreshToken = asString(body.refreshToken);
    if (!refreshToken) {
      res.status(400).json({ error: 'missing_refresh_token', message: 'refreshToken is required' });
      return;
    }

    const session = findSessionByRefreshToken(db, refreshToken);
    if (!session) {
      res.status(401).json({ error: 'invalid_refresh_token', message: 'Refresh token is not recognised' });
      return;
    }

    if (session.revoked_at !== null) {
      const revoked = revokeAllSessionsForUser(db, session.user_id, {
        reason: 'refresh_token_reuse',
      });
      res.status(401).json({
        error: 'refresh_token_reuse',
        message: 'This refresh token was already revoked. All sessions have been signed out.',
        revokedCount: revoked,
      });
      return;
    }

    if (!isActive(session)) {
      res.status(401).json({ error: 'session_expired', message: 'Session has expired. Sign in again.' });
      return;
    }

    const user = findUserById(db, session.user_id);
    if (!user) {
      res.status(401).json({ error: 'invalid_refresh_token', message: 'Refresh token is not recognised' });
      return;
    }

    const rotated = rotateRefreshToken(db, session.id);
    res.json({
      accessToken: signAccessToken(
        { sub: user.id, sid: session.id },
        config.jwtSecret,
        config.accessTokenTtlSeconds,
      ),
      refreshToken: rotated,
      sessionId: session.id,
      expiresIn: config.accessTokenTtlSeconds,
    });
  });

  router.get('/auth/sessions', auth, (req: Request, res: Response): void => {
    const { userId, sessionId } = req.auth!;
    res.json({
      sessions: listActiveSessions(db, userId).map((row) => toPublicSession(row, sessionId)),
    });
  });

  router.post('/auth/logout', auth, (req: Request, res: Response): void => {
    const { sessionId } = req.auth!;
    revokeSession(db, sessionId, 'logout');
    res.json({ ok: true, revokedCount: 1 });
  });

  /** Revoke one other device without disturbing the rest. */
  router.delete('/auth/sessions/:id', auth, (req: Request, res: Response): void => {
    const { userId, sessionId } = req.auth!;
    const targetId = req.params.id as string;

    const target = findSessionById(db, targetId);
    // Same 404 whether the session belongs to someone else or does not exist,
    // so session ids cannot be probed across accounts.
    if (!target || target.user_id !== userId) {
      res.status(404).json({ error: 'session_not_found', message: 'No such session' });
      return;
    }

    const revoked = revokeSession(db, targetId, 'revoked_by_user');
    res.json({ ok: true, revokedCount: revoked ? 1 : 0, wasCurrent: targetId === sessionId });
  });

  /**
   * Log out of all devices.
   *
   * Body: `{ "keepCurrent": true }` to stay signed in here. The default signs
   * out everything, this device included — that is what "all devices" says.
   */
  router.post('/auth/logout-all', auth, (req: Request, res: Response): void => {
    const { userId, sessionId } = req.auth!;
    const body = (req.body ?? {}) as Record<string, unknown>;
    const keepCurrent = body.keepCurrent === true;

    const revokedCount = revokeAllSessionsForUser(db, userId, {
      exceptSessionId: keepCurrent ? sessionId : null,
      reason: 'logout_all',
    });

    res.json({ ok: true, revokedCount, keptCurrent: keepCurrent });
  });

  return router;
}
