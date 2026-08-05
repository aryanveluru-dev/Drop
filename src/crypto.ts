import {
  createHash,
  createHmac,
  randomBytes,
  scryptSync,
  timingSafeEqual,
} from 'node:crypto';

const SCRYPT_KEYLEN = 64;
const SCRYPT_N = 16384;
const SCRYPT_R = 8;
const SCRYPT_P = 1;

/** Encodes as `scrypt$N$r$p$salt$hash` so parameters can be raised without breaking old hashes. */
export function hashPassword(password: string): string {
  const salt = randomBytes(16);
  const derived = scryptSync(password, salt, SCRYPT_KEYLEN, {
    N: SCRYPT_N,
    r: SCRYPT_R,
    p: SCRYPT_P,
  });
  return [
    'scrypt',
    SCRYPT_N,
    SCRYPT_R,
    SCRYPT_P,
    salt.toString('base64'),
    derived.toString('base64'),
  ].join('$');
}

export function verifyPassword(password: string, stored: string): boolean {
  const parts = stored.split('$');
  if (parts.length !== 6 || parts[0] !== 'scrypt') return false;

  const n = Number(parts[1]);
  const r = Number(parts[2]);
  const p = Number(parts[3]);
  if (![n, r, p].every((value) => Number.isInteger(value) && value > 0)) return false;

  const salt = Buffer.from(parts[4]!, 'base64');
  const expected = Buffer.from(parts[5]!, 'base64');
  if (expected.length === 0) return false;

  let derived: Buffer;
  try {
    derived = scryptSync(password, salt, expected.length, { N: n, r, p });
  } catch {
    return false;
  }
  return derived.length === expected.length && timingSafeEqual(derived, expected);
}

export interface AccessTokenClaims {
  /** User id. */
  sub: string;
  /** Session id — the link that makes a token revocable. */
  sid: string;
  iat: number;
  exp: number;
}

function base64urlJson(value: unknown): string {
  return Buffer.from(JSON.stringify(value), 'utf8').toString('base64url');
}

export function signAccessToken(
  claims: Pick<AccessTokenClaims, 'sub' | 'sid'>,
  secret: string,
  ttlSeconds: number,
  now: number = Date.now(),
): string {
  const issuedAt = Math.floor(now / 1000);
  const header = base64urlJson({ alg: 'HS256', typ: 'JWT' });
  const payload = base64urlJson({
    sub: claims.sub,
    sid: claims.sid,
    iat: issuedAt,
    exp: issuedAt + ttlSeconds,
  });
  const signingInput = `${header}.${payload}`;
  const signature = createHmac('sha256', secret).update(signingInput).digest('base64url');
  return `${signingInput}.${signature}`;
}

/**
 * Verifies signature and expiry only. Callers must still confirm the session
 * named by `sid` is live — that check is what makes revocation immediate.
 */
export function verifyAccessToken(
  token: string,
  secret: string,
  now: number = Date.now(),
): AccessTokenClaims | null {
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [encodedHeader, encodedPayload, encodedSignature] = parts as [string, string, string];

  const expected = createHmac('sha256', secret)
    .update(`${encodedHeader}.${encodedPayload}`)
    .digest();
  const actual = Buffer.from(encodedSignature, 'base64url');
  if (actual.length !== expected.length || !timingSafeEqual(actual, expected)) return null;

  let header: unknown;
  let claims: unknown;
  try {
    header = JSON.parse(Buffer.from(encodedHeader, 'base64url').toString('utf8'));
    claims = JSON.parse(Buffer.from(encodedPayload, 'base64url').toString('utf8'));
  } catch {
    return null;
  }

  if ((header as { alg?: unknown } | null)?.alg !== 'HS256') return null;

  const candidate = claims as Partial<AccessTokenClaims> | null;
  if (
    typeof candidate?.sub !== 'string' ||
    typeof candidate.sid !== 'string' ||
    typeof candidate.iat !== 'number' ||
    typeof candidate.exp !== 'number'
  ) {
    return null;
  }
  if (candidate.exp * 1000 <= now) return null;

  return candidate as AccessTokenClaims;
}

/** Opaque refresh token — never a JWT, so it carries no authority of its own. */
export function generateRefreshToken(): string {
  return randomBytes(32).toString('base64url');
}

export function sha256(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}
