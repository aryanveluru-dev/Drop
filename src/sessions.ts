import { randomUUID } from 'node:crypto';
import type { Database } from './db.js';
import { generateRefreshToken, sha256 } from './crypto.js';

export interface SessionRow {
  id: string;
  user_id: string;
  refresh_token_hash: string;
  device_label: string | null;
  user_agent: string | null;
  ip: string | null;
  created_at: number;
  last_seen_at: number;
  expires_at: number;
  revoked_at: number | null;
  revoked_reason: string | null;
}

export interface PublicSession {
  id: string;
  deviceLabel: string | null;
  userAgent: string | null;
  ip: string | null;
  createdAt: string;
  lastSeenAt: string;
  expiresAt: string;
  /** True for the session making the request, so a UI can label "This device". */
  current: boolean;
}

export type RevocationReason =
  | 'logout'
  | 'logout_all'
  | 'revoked_by_user'
  | 'refresh_token_reuse';

export interface DeviceContext {
  deviceLabel?: string | null;
  userAgent?: string | null;
  ip?: string | null;
}

export function toPublicSession(row: SessionRow, currentSessionId: string | null): PublicSession {
  return {
    id: row.id,
    deviceLabel: row.device_label,
    userAgent: row.user_agent,
    ip: row.ip,
    createdAt: new Date(row.created_at).toISOString(),
    lastSeenAt: new Date(row.last_seen_at).toISOString(),
    expiresAt: new Date(row.expires_at).toISOString(),
    current: row.id === currentSessionId,
  };
}

export function isActive(session: SessionRow, now = Date.now()): boolean {
  return session.revoked_at === null && session.expires_at > now;
}

export function createSession(
  db: Database,
  userId: string,
  ttlSeconds: number,
  device: DeviceContext = {},
  now = Date.now(),
): { session: SessionRow; refreshToken: string } {
  const refreshToken = generateRefreshToken();
  const session: SessionRow = {
    id: randomUUID(),
    user_id: userId,
    refresh_token_hash: sha256(refreshToken),
    device_label: device.deviceLabel ?? null,
    user_agent: device.userAgent ?? null,
    ip: device.ip ?? null,
    created_at: now,
    last_seen_at: now,
    expires_at: now + ttlSeconds * 1000,
    revoked_at: null,
    revoked_reason: null,
  };

  db.prepare(
    `INSERT INTO sessions (
       id, user_id, refresh_token_hash, device_label, user_agent, ip,
       created_at, last_seen_at, expires_at, revoked_at, revoked_reason
     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)`,
  ).run(
    session.id,
    session.user_id,
    session.refresh_token_hash,
    session.device_label,
    session.user_agent,
    session.ip,
    session.created_at,
    session.last_seen_at,
    session.expires_at,
  );

  return { session, refreshToken };
}

export function findSessionById(db: Database, id: string): SessionRow | undefined {
  return db.prepare('SELECT * FROM sessions WHERE id = ?').get(id) as SessionRow | undefined;
}

/** Looks up by hash — the raw refresh token is never stored. */
export function findSessionByRefreshToken(db: Database, token: string): SessionRow | undefined {
  return db.prepare('SELECT * FROM sessions WHERE refresh_token_hash = ?').get(sha256(token)) as
    | SessionRow
    | undefined;
}

export function listActiveSessions(db: Database, userId: string, now = Date.now()): SessionRow[] {
  return db
    .prepare(
      `SELECT * FROM sessions
        WHERE user_id = ? AND revoked_at IS NULL AND expires_at > ?
        ORDER BY last_seen_at DESC`,
    )
    .all(userId, now) as unknown as SessionRow[];
}

/** Throttled by the caller so a busy device does not write on every request. */
export function touchSession(db: Database, id: string, now = Date.now()): void {
  db.prepare('UPDATE sessions SET last_seen_at = ? WHERE id = ?').run(now, id);
}

export function rotateRefreshToken(db: Database, sessionId: string): string {
  const refreshToken = generateRefreshToken();
  db.prepare('UPDATE sessions SET refresh_token_hash = ? WHERE id = ?').run(
    sha256(refreshToken),
    sessionId,
  );
  return refreshToken;
}

/** Returns false if the session was already revoked. */
export function revokeSession(
  db: Database,
  id: string,
  reason: RevocationReason,
  now = Date.now(),
): boolean {
  const result = db
    .prepare(
      'UPDATE sessions SET revoked_at = ?, revoked_reason = ? WHERE id = ? AND revoked_at IS NULL',
    )
    .run(now, reason, id);
  return Number(result.changes) > 0;
}

/**
 * Signs a user out everywhere. This is the whole point of the session table:
 * because every authenticated request re-reads its session row, tokens already
 * issued to other devices stop working on the next request rather than when
 * they expire.
 *
 * @param exceptSessionId keep this one session alive (the "except this device" case)
 * @returns how many sessions were revoked
 */
export function revokeAllSessionsForUser(
  db: Database,
  userId: string,
  options: { exceptSessionId?: string | null; reason?: RevocationReason } = {},
  now = Date.now(),
): number {
  const { exceptSessionId = null, reason = 'logout_all' } = options;

  const result = exceptSessionId
    ? db
        .prepare(
          `UPDATE sessions SET revoked_at = ?, revoked_reason = ?
            WHERE user_id = ? AND revoked_at IS NULL AND id != ?`,
        )
        .run(now, reason, userId, exceptSessionId)
    : db
        .prepare(
          `UPDATE sessions SET revoked_at = ?, revoked_reason = ?
            WHERE user_id = ? AND revoked_at IS NULL`,
        )
        .run(now, reason, userId);

  return Number(result.changes);
}

/** Housekeeping: drop rows that are long past use. Safe to run on a schedule. */
export function purgeExpiredSessions(db: Database, olderThan: number): number {
  const result = db.prepare('DELETE FROM sessions WHERE expires_at < ?').run(olderThan);
  return Number(result.changes);
}
