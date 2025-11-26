Database design (conceptual blueprint & decisions you must make)
================================================================

### Core tables (names + purpose)

*   **users** — central user account (auth info, email, password hash, status flags).
    
*   **profiles** — optional 1:1 user metadata (display name, avatar url, bio) — keeps auth separate from profile data.
    
*   **roles** — named roles (e.g., admin, user, manager).
    
*   **user\_roles** — many-to-many join between users and roles.
    
*   **permissions** (optional) — fine-grained actions, or use role-based simple model.
    
*   **refresh\_tokens** — store issued refresh tokens (if you use server-side rotation/session).
    
*   **audit\_logs** — record important events (login, failed login, user update, admin actions).
    
*   **password\_resets** — one-time tokens for resetting passwords.
    
*   **rate\_limits** (optional) — track request counts per IP/user for throttling.
    

### Key conceptual fields (no SQL, just what to include)

*   users: id (PK, integer or UUID), email (unique, indexed), password\_hash, is\_active (boolean), created\_at, updated\_at, last\_login\_at, failed\_login\_attempts, locked\_until (nullable).
    
*   profiles: user\_id (FK → users.id), full\_name, avatar\_path, phone (unique optional), address\_json (if needed).
    
*   roles: id, name (unique), description.
    
*   user\_roles: user\_id FK, role\_id FK, assigned\_at.
    
*   refresh\_tokens: id, user\_id FK, token\_hash (store hash of the token), issued\_at, expires\_at, revoked (bool), replaced\_by (nullable FK).
    
*   audit\_logs: id, user\_id (nullable), event\_type, event\_data (JSON), ip\_address, occurred\_at.
    

### Relational and integrity rules

*   Use **foreign keys** for referential integrity.
    
*   Enforce **unique constraints** on email and any identifier fields.
    
*   Consider **soft deletes** (e.g., is\_deleted or deleted\_at) vs hard deletes — prefer soft delete for users for safety.
    
*   **Normalize** to at least 3NF: keep authentication data (password hash) separate from profile/metadata.
    

### Indexing strategy (conceptual)

*   Index columns used in lookups: email, user\_id for joins, created\_at if sorting by recency.
    
*   Composite index for common queries (example: user\_id + created\_at in audit\_logs if you query logs per user sorted by time).
    
*   Don’t over-index — each index costs writes.
    

### Security-focused DB notes

*   **Never store plain tokens or passwords** — store password hashes (with a modern algorithm) and **hash refresh tokens** too.
    
*   Keep jwt secret out of source control (env var / secrets manager).
    
*   Consider storing a token version or session\_id to invalidate existing JWTs on password change.
    

Backend design (architecture & API contracts — no code)
=======================================================

### Architectural layers (conceptual)

*   **Router / Controller**: HTTP layer — parse request, call service, return response.
    
*   **Service (business logic)**: orchestrates operations (validation beyond request-level, transactions, calling repo).
    
*   **Repository / DAO**: DB access (single place for SQL/ORM).
    
*   **Schemas / DTOs**: request/response shapes and validation.
    
*   **Utilities**: security (hashing, token creation), email, logging.
    

### Essential endpoints (list + purpose — design these exact routes)

*   POST /auth/register — register new user (validate email, password complexity, create user & profile, send verify email).
    
*   POST /auth/login — authenticate credentials → return access token (JWT) + refresh token (if used).
    
*   POST /auth/refresh — exchange refresh token for new access token (and optionally a new refresh token).
    
*   POST /auth/logout — revoke refresh token or clear session.
    
*   POST /auth/request-password-reset — initiate reset, send email with one-time token.
    
*   POST /auth/reset-password — consume reset token, update password (invalidate sessions).
    
*   GET /users — list users (admin, supports pagination, filters).
    
*   GET /users/{id} — get user (profile) details.
    
*   PATCH /users/{id} — update user metadata (admin or owner).
    
*   DELETE /users/{id} — soft delete or mark as disabled (admin).
    
*   GET /me — current user profile (requires auth).
    

For each endpoint define:

*   Required auth (none, bearer, admin-only).
    
*   Accepts: what fields exactly (names + whether required).
    
*   Returns: what shape (omit sensitive fields).
    
*   Error cases and status codes (400 validation, 401 unauthorized, 403 forbidden, 404 not found, 409 conflict on duplicate email).
    

### Auth flow (conceptual)

*   On login: verify password, create access JWT with short expiry (e.g., minutes) and issue refresh token with longer expiry (days/weeks).
    
*   Store refresh token server-side hashed (so you can revoke/rotate).
    
*   Access token used in Authorization: Bearer header for protected routes.
    
*   On password change or logout, revoke refresh tokens, and optionally keep a token\_version on user to make old JWTs invalid if you embed it in token claims.
    

### Validation & error handling

*   Validate at both schema level and service level (business rules).
    
*   Return consistent error format (error code, message, details).
    
*   Log server errors with correlation id; do not leak internal errors to client.
    

Frontend design (conceptual, React/Vite)
========================================

### High-level app structure

*   **Pages**: Login, Register, Dashboard (protected), Users List (admin), User Profile, Settings, NotFound.
    
*   **Components**: Form components (input, select), Modal, Table with pagination, ProtectedRoute wrapper, Header/Nav, Toasts/Alerts.
    
*   **State**: Auth context/provider with user state and token info; pages fetch via service layer (api.js conceptually).
    

### Auth handling options (compare pros/cons)

*   **HttpOnly cookies (recommended)**: access token or refresh token in secure, httpOnly cookie — safer against XSS. Needs CSRF protection if cookies used for auth.
    
*   **localStorage/sessionStorage**: easier to implement but vulnerable to XSS (not recommended for refresh tokens).
    
*   My suggestion: store access token in memory and refresh via httpOnly refresh token cookie. (I won’t write code — you must implement and test)
    
*   Protect routes by checking auth context + trying token refresh if necessary.
    

### UX & forms

*   Client-side validation mirroring server rules — don’t trust client though.
    
*   Show friendly error messages for validation, server errors, and connectivity issues.
    
*   Implement optimistic updates carefully (only for low-stakes UX).
    

Testing, debugging, and QA (what you must do)
=============================================

*   **Unit tests** for service logic (auth checks, permission checks).
    
*   **Integration tests** for API endpoints (use an isolated test DB; test happy and unhappy paths).
    
*   **Manual API tests** using Postman / Insomnia: cover login, token refresh, protected route access.
    
*   **Frontend E2E** (optional later) to run flows: login → view profile → update.
    
*   **Failure tests**: invalid token, expired refresh, reused refresh, concurrent logins.
    
*   **Load concern**: simulate many logins to see DB index and locking behavior.
    

Security checklist (you will implement and test)
================================================

*   Password policy (min length, complexity).
    
*   Hash passwords (modern algorithm, salts).
    
*   Rate-limit login endpoints; block IPs after repeated failures.
    
*   Use HTTPS in deployment.
    
*   Store secrets out of code (env / secret manager).
    
*   Validate JWT signature and expiry, check token versions on sensitive actions.
    
*   Sanitize and validate all user input to avoid SQL injection (use prepared statements/ORM).
    
*   Avoid returning raw DB errors to clients.