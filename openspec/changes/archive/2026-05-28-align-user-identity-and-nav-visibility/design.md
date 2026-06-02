## Context

The application currently stores both `username` and `nickname` on `users`. Registration asks for both, login uses `username`, and most content displays `nickname`. This is functional but confusing because users must invent two names before entering the system.

Navigation is driven by a flat route list in `frontend/src/routes/route-config.js`; `AppLayout` renders slices of that list for every visitor. Private pages still use route guards, so guests cannot use quick notes or drafts, but those entries remain visible and then redirect to login.

## Goals / Non-Goals

**Goals:**
- Present a single user name field during registration and account display.
- Keep existing backend auth/token/database shape compatible with existing users and code.
- Ensure new users have `username` and `nickname` initialized consistently from the one registration name.
- Filter navigation by user state so guests only see usable public/login/register entries, while authenticated users see private tools.
- Keep direct URL protection for private pages.

**Non-Goals:**
- Renaming the database columns or dropping either `username` or `nickname`.
- Migrating existing usernames to new values.
- Adding role-based admin navigation beyond guest/authenticated visibility.
- Changing password, token, or session mechanics.

## Decisions

1. Keep `username` as the login identifier and treat `nickname` as the display alias internally.

   The merged UI will submit one field, but the backend will continue storing both values. This avoids a destructive SQLite migration and keeps existing API consumers, token payloads, and relationships stable. New registrations will pass the same sanitized name as `username` and `nickname`.

   Alternative considered: remove `nickname` from the schema. Rejected because author/comment/photo/follow displays already depend on nickname, and removing it would create broad schema churn for little user benefit.

2. Add backend compatibility for old and new registration payloads.

   `RegisterRequest` should allow the new single-name payload while still accepting the old `nickname` field during transition. The API will derive `nickname = provided nickname or username`. The frontend will send only the merged name, but old clients will not break.

   Alternative considered: require only the new payload immediately. Rejected because the current app and any existing manual API calls may still send `nickname`.

3. Update visible UI language instead of hiding all internal identity fields.

   Registration should show one account/name input. Profile and relation displays should use the merged display name as the primary label. Where the raw login identifier is still useful, it may remain as secondary technical text only if it differs from the display name; for newly registered users it should not duplicate the same string.

   Alternative considered: keep showing both names everywhere but auto-fill nickname. Rejected because it does not solve the visible duplication.

4. Add route visibility metadata and filter navigation from auth state.

   Route config will get a `visibility` field such as `public`, `guest`, or `auth`. `AppLayout` will compute visible nav routes using `isAuthenticated`, then render the filtered list. Pages like quick notes, profile, settings, drafts, editor, follows, and private management tools will be `auth`; login/register will be `guest`; public reading areas will be `public`.

   Alternative considered: keep all nav links and rely only on `ProtectedRoute`. Rejected because the user's requirement is to show only usable parts, not just block access.

5. Keep route guards as the security boundary.

   Navigation filtering is a UX rule, not authorization. `ProtectedRoute` stays on private routes so direct URL entry, stale tabs, and copied links remain protected.

   Alternative considered: remove guards once links are hidden. Rejected because hidden navigation cannot protect direct requests.

## Risks / Trade-offs

- Existing users may still have different `username` and `nickname` values -> Display rules should avoid showing duplicate labels only when values are equal, and otherwise preserve existing identity information.
- Single-name registration still needs a valid login identifier -> The input must keep the current username constraints unless a later change adds separate display-name normalization.
- Hidden links can make discovery harder for guests -> Public pages should still include login/register entry points, and protected redirects remain available for direct URLs.
- Route visibility metadata can drift from `privatePaths` -> Implementation should keep route guard and nav metadata close together or derive both from route config where practical.

## Migration Plan

1. Deploy backend compatibility first: derive missing nickname from username on registration.
2. Update frontend registration/profile/relation displays to use the merged identity presentation.
3. Add route visibility metadata and filter navigation for guest/authenticated states.
4. Verify guests do not see quick notes/private tools, logged-in users do, and manual private URL entry still redirects when logged out.

Rollback is straightforward because no database columns are removed: revert frontend UI filtering and backend schema compatibility if needed.

## Open Questions

- Should existing users with different `username` and `nickname` be offered an explicit one-time merge action later, or simply keep both internally?
