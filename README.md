# Drop

Account and device-session management, with first-class support for **signing out of every device at once**.

## Why this is more than a `DELETE`

Signing out everywhere is easy to get subtly wrong. If access tokens are self-contained JWTs that the server trusts on sight, "log out of all devices" cannot actually log anything out — a stolen token keeps working until it expires. A 15-minute window after a user hits the panic button is not a logout.

Drop closes that window. Every access token carries a session id (`sid`), and every authenticated request re-reads that session row before doing anything. Revoking the row takes effect on the *next request*, not at token expiry.

The cost is one indexed primary-key lookup per authenticated request. That is the price of real revocation, and for a session table it is a price worth paying.

## Quick start

```bash
npm install
npm test          # 16 tests, no network or fixtures required
npm run build
AUTH_JWT_SECRET=$(openssl rand -hex 32) npm start
```

Requires Node **22.5+** — storage uses the built-in `node:sqlite`, so the only runtime dependency is Express. Node prints an experimental-feature warning for `node:sqlite`; that is expected.

## API

| Method   | Path                   | Auth | Purpose                                    |
| -------- | ---------------------- | ---- | ------------------------------------------ |
| `POST`   | `/auth/register`       | —    | Create an account, sign in                 |
| `POST`   | `/auth/login`          | —    | Sign in, opening a new session             |
| `POST`   | `/auth/refresh`        | —    | Exchange a refresh token (rotates it)      |
| `GET`    | `/auth/sessions`       | ✓    | List signed-in devices                     |
| `POST`   | `/auth/logout`         | ✓    | Sign out this device only                  |
| `DELETE` | `/auth/sessions/:id`   | ✓    | Sign out one other device                  |
| `POST`   | `/auth/logout-all`     | ✓    | **Sign out of all devices**                |

Authenticate with `Authorization: Bearer <accessToken>`.

### Log out of all devices

```bash
curl -X POST http://localhost:3000/auth/logout-all \
  -H "authorization: Bearer $ACCESS_TOKEN" \
  -H 'content-type: application/json' \
  -d '{}'
```

```json
{ "ok": true, "revokedCount": 3, "keptCurrent": false }
```

The default signs out **everything, this device included** — that is what "all devices" says, and it is the right default for the case where you hit this because a device was lost. To stay signed in where you are:

```json
{ "keepCurrent": true }
```

### Listing devices

`GET /auth/sessions` returns active sessions with the device label, user agent, IP, and timestamps, with `current: true` on the calling session so a settings screen can label "This device". Token material is never returned.

## How it works

**Two token types, deliberately different.**

- *Access token* — a short-lived (15 min) HS256 JWT holding `sub` (user) and `sid` (session). Stateless to verify, but never trusted alone.
- *Refresh token* — 32 opaque random bytes, stored only as a SHA-256 hash. It carries no claims, so it grants nothing by itself.

**Revocation is a row, not a deletion.** Signing out sets `revoked_at`; the row stays. That is what makes the next property possible.

**Refresh tokens rotate, and reuse is treated as a breach.** Each refresh issues a new token and invalidates the old one. If a token belonging to an *already-revoked* session shows up, that token leaked after the session ended — so Drop signs out every session for that user and says so:

```json
{ "error": "refresh_token_reuse", "revokedCount": 2 }
```

This is why the test suite asserts that an innocent bystander device also gets signed out. That is intended: a confirmed leak is worth one forced re-login.

**Passwords** use scrypt (N=16384, r=8, p=1) with a per-password salt, verified with `timingSafeEqual`. Parameters are encoded in the stored hash, so they can be raised later without invalidating existing passwords. Login runs a decoy hash for unknown emails so response timing does not reveal which addresses have accounts.

**Cross-account probing** is blocked: revoking a session id that belongs to another user returns the same `404` as one that does not exist.

## Configuration

| Variable                 | Default   | Notes                                            |
| ------------------------ | --------- | ------------------------------------------------ |
| `PORT`                   | `3000`    |                                                  |
| `DATABASE_PATH`          | `drop.db` | `:memory:` works for tests                       |
| `AUTH_JWT_SECRET`        | dev value | **Required in production** — startup fails without it |
| `ACCESS_TOKEN_TTL`       | `900`     | Seconds                                          |
| `REFRESH_TOKEN_TTL`      | `2592000` | Seconds (30 days)                                |
| `SESSION_TOUCH_INTERVAL` | `60`      | Seconds before `last_seen_at` is rewritten       |

## Not included

Deliberately out of scope, and worth adding before this faces real traffic:

- **Rate limiting** on `/auth/login` and `/auth/refresh` — nothing here slows down credential stuffing.
- **Password change and reset**, which should revoke all other sessions on success.
- **Email notification** when sessions are revoked in bulk, so the user learns about a logout they did not perform.
- **Purging old rows** — `purgeExpiredSessions()` exists in `src/sessions.ts` but nothing schedules it.
- **Refresh tokens in httpOnly cookies** rather than response bodies, if a browser client is added.
