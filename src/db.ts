import { DatabaseSync } from 'node:sqlite';

export type Database = DatabaseSync;

const SCHEMA = `
CREATE TABLE IF NOT EXISTS users (
  id            TEXT PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at    INTEGER NOT NULL
);

-- One row per signed-in device. Rows are never deleted on logout: a revoked
-- row is what lets us recognise a replayed refresh token after the fact.
CREATE TABLE IF NOT EXISTS sessions (
  id                 TEXT PRIMARY KEY,
  user_id            TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  refresh_token_hash TEXT NOT NULL UNIQUE,
  device_label       TEXT,
  user_agent         TEXT,
  ip                 TEXT,
  created_at         INTEGER NOT NULL,
  last_seen_at       INTEGER NOT NULL,
  expires_at         INTEGER NOT NULL,
  revoked_at         INTEGER,
  revoked_reason     TEXT
);

CREATE INDEX IF NOT EXISTS sessions_user_id_idx ON sessions (user_id);
CREATE INDEX IF NOT EXISTS sessions_active_idx ON sessions (user_id, revoked_at);
`;

export function openDatabase(path: string): Database {
  const db = new DatabaseSync(path);
  if (path !== ':memory:') db.exec('PRAGMA journal_mode = WAL');
  db.exec('PRAGMA foreign_keys = ON');
  db.exec(SCHEMA);
  return db;
}
