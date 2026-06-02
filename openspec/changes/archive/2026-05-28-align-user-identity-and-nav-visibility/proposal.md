## Why

The current user identity model exposes both username and nickname in the UI, which creates unnecessary duplicate input and inconsistent display. Navigation also lists private features such as quick notes for users who cannot use them, relying on route blocking instead of showing only relevant entry points.

## What Changes

- Merge the registration-facing username and nickname concept so users enter one display/account name instead of two visible names.
- Keep backend authentication stable while ensuring newly registered users have consistent `username` and `nickname` values derived from the single input.
- Update profile and relation displays so the primary user label is the merged user name, avoiding redundant `@username` treatment where it no longer helps.
- Make the top navigation state-aware:
  - Guests see only public browsing and login/register entries.
  - Logged-in users see personal tools such as profile, settings, editor drafts, quick notes, follows, and manageable content areas.
  - Private tools such as quick notes are hidden from guests instead of appearing and redirecting to login.
- Preserve direct route protection for private pages even if a user manually enters a URL.

## Capabilities

### New Capabilities
- `user-identity-navigation`: Covers merged user naming behavior and navigation visibility by current user state.

### Modified Capabilities

## Impact

- Frontend auth pages, profile page, relation/user displays, route metadata, and layout navigation filtering.
- Backend registration schema/service behavior for assigning nickname from the merged name.
- Existing auth/login APIs remain available; database schema should avoid destructive user data migration unless design determines it is necessary.
