export interface Config {
  port: number;
  databasePath: string;
  jwtSecret: string;
  /** Access tokens are short-lived; revocation does not wait for them to expire. */
  accessTokenTtlSeconds: number;
  refreshTokenTtlSeconds: number;
  /** How stale `last_seen_at` may get before an authenticated request rewrites it. */
  sessionTouchIntervalSeconds: number;
}

const DEV_SECRET = 'dev-only-insecure-secret-do-not-use-in-production';

function intFromEnv(raw: string | undefined, fallback: number, name: string): number {
  if (raw === undefined || raw === '') return fallback;
  const value = Number(raw);
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(`${name} must be a positive integer, got ${JSON.stringify(raw)}`);
  }
  return value;
}

export function loadConfig(env: NodeJS.ProcessEnv = process.env): Config {
  const isProduction = env.NODE_ENV === 'production';
  const secret = env.AUTH_JWT_SECRET;

  if (isProduction && (!secret || secret === DEV_SECRET)) {
    throw new Error('AUTH_JWT_SECRET must be set to a strong random value in production');
  }

  return {
    port: intFromEnv(env.PORT, 3000, 'PORT'),
    databasePath: env.DATABASE_PATH ?? 'drop.db',
    jwtSecret: secret || DEV_SECRET,
    accessTokenTtlSeconds: intFromEnv(env.ACCESS_TOKEN_TTL, 15 * 60, 'ACCESS_TOKEN_TTL'),
    refreshTokenTtlSeconds: intFromEnv(env.REFRESH_TOKEN_TTL, 30 * 24 * 60 * 60, 'REFRESH_TOKEN_TTL'),
    sessionTouchIntervalSeconds: intFromEnv(env.SESSION_TOUCH_INTERVAL, 60, 'SESSION_TOUCH_INTERVAL'),
  };
}
