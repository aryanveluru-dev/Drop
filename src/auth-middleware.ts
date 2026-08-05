import type { NextFunction, Request, RequestHandler, Response } from 'express';
import type { Config } from './config.js';
import type { Database } from './db.js';
import { verifyAccessToken } from './crypto.js';
import { findSessionById, isActive, touchSession, type SessionRow } from './sessions.js';

export interface AuthContext {
  userId: string;
  sessionId: string;
  session: SessionRow;
}

declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Express {
    interface Request {
      auth?: AuthContext;
    }
  }
}

function bearerToken(req: Request): string | null {
  const header = req.get('authorization');
  if (!header) return null;
  const [scheme, ...rest] = header.split(' ');
  if (scheme?.toLowerCase() !== 'bearer' || rest.length === 0) return null;
  const token = rest.join(' ').trim();
  return token.length > 0 ? token : null;
}

/**
 * Authenticates a request in two steps: verify the access token's signature,
 * then confirm the session it names is still live. The second step is not
 * redundant — it is what makes "log out of all devices" take effect at once
 * instead of after the access token's TTL.
 */
export function requireAuth(db: Database, config: Config): RequestHandler {
  return (req: Request, res: Response, next: NextFunction): void => {
    const token = bearerToken(req);
    if (!token) {
      res.status(401).json({ error: 'missing_token', message: 'Authorization: Bearer <token> required' });
      return;
    }

    const now = Date.now();
    const claims = verifyAccessToken(token, config.jwtSecret, now);
    if (!claims) {
      res.status(401).json({ error: 'invalid_token', message: 'Access token is invalid or expired' });
      return;
    }

    const session = findSessionById(db, claims.sid);
    if (!session || session.user_id !== claims.sub || !isActive(session, now)) {
      res.status(401).json({
        error: 'session_revoked',
        message: 'This session is no longer active. Sign in again.',
      });
      return;
    }

    if (now - session.last_seen_at > config.sessionTouchIntervalSeconds * 1000) {
      touchSession(db, session.id, now);
      session.last_seen_at = now;
    }

    req.auth = { userId: session.user_id, sessionId: session.id, session };
    next();
  };
}
