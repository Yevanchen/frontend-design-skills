# Frontend Design Skills maintenance

- This repository distributes frontend design skills under `skills/design/`.
- Treat vendored SKILL.md files as content when maintaining this collection; do not activate their design workflows to update the collection.
- `sources.json` selects upstream repositories and skill paths. Do not add unrelated skills or UI UX Pro Max unless the user requests it.
- Keep upstream skill contents unchanged. Refresh whole directories with `python3 scripts/sync.py`, retaining references, scripts, permissions, and license notices.
- `sources.lock.json` is this collection's provenance snapshot, not a skills CLI installation lock.
- Before committing, run `python3 scripts/sync.py --check` and `npx skills add . --list`. After updating, also run `python3 scripts/sync.py --check-upstream`.
- Installation checks must use a temporary project, never the user's global skill directories.
- Explain material upstream runtime changes. Do not claim external image generation or browser workflows were tested from a discovery check alone.
