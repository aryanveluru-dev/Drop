import { randomUUID } from 'node:crypto';
import type { Database } from './db.js';
import { hashPassword, verifyPassword } from './crypto.js';

export interface UserRow {
  id: string;
  email: string;
  password_hash: string;
  created_at: number;
}

export class EmailTakenError extends Error {
  constructor(email: string) {
    super(`An account already exists for ${email}`);
    this.name = 'EmailTakenError';
  }
}

export function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

export function createUser(db: Database, email: string, password: string, now = Date.now()): UserRow {
  const row: UserRow = {
    id: randomUUID(),
    email: normalizeEmail(email),
    password_hash: hashPassword(password),
    created_at: now,
  };
  try {
    db.prepare(
      'INSERT INTO users (id, email, password_hash, created_at) VALUES (?, ?, ?, ?)',
    ).run(row.id, row.email, row.password_hash, row.created_at);
  } catch (error) {
    if (String((error as Error).message).includes('UNIQUE')) {
      throw new EmailTakenError(row.email);
    }
    throw error;
  }
  return row;
}

export function findUserByEmail(db: Database, email: string): UserRow | undefined {
  return db.prepare('SELECT * FROM users WHERE email = ?').get(normalizeEmail(email)) as
    | UserRow
    | undefined;
}

export function findUserById(db: Database, id: string): UserRow | undefined {
  return db.prepare('SELECT * FROM users WHERE id = ?').get(id) as UserRow | undefined;
}

/**
 * Verifies credentials in constant-ish time: an unknown email still pays for a
 * password hash, so response timing does not disclose which emails exist.
 */
export function authenticate(db: Database, email: string, password: string): UserRow | null {
  const user = findUserByEmail(db, email);
  if (!user) {
    verifyPassword(password, hashPassword('decoy-password'));
    return null;
  }
  return verifyPassword(password, user.password_hash) ? user : null;
}
