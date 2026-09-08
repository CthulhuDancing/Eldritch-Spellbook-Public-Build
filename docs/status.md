# Project Status

## Version

`0.13.0` - Application data and secrets

## Current phase

Validate the eight-skill plugin from its public repository.

## Completed

- Replaced Morph-specific discovery guidance with a native-first, tool-optional workflow.
- Kept codebase discovery implicit for unfamiliar or scattered behavior while preferring exact native search for known targets.
- Kept routine-worktree suitability discoverable for users who may not know which workflow to request.
- Made agent handoff preparation discoverable and split it into project and targeted-task lanes.
- Enabled natural-language selection for explicitly requested GitHub actions,
  without inferring permission to write from skill selection.
- Added provider-neutral `fix-ci` guidance that implicitly diagnoses failing automated checks and separates code defects from environment or external failures.
- Removed machine-specific paths, fixed worktree locations, and shared-tooling assumptions.
- Preserved user-controlled boundaries for consequential GitHub and agent actions.
- Initialized the clean public repository with fresh Git history.
- Added a narrowly gated local-workspace bootstrap workflow that reuses
  documented runtimes, tools, caches, and worktree conventions before
  attempting replacement.
- Added a routine-worktree policy fast path so clear local guidance is reused
  without repeated instruction audits.
- Added a dedicated read-only workflow for external public source and
  dependency-internals research, separate from local codebase discovery.
- Narrowed handoffs to actual context transfers, aligned bootstrap entry points,
  and separated instruction ownership from precedence.
- Added a safe fresh-user bootstrap fallback and discoverable local-policy
  recording, while retaining fast-path reuse and scoped authorization.
- Allowed suitable existing task worktrees to be reused and kept trivial local
  edits outside the full delivery workflow unless that workflow is required.
- Added application data and secrets guidance with conditional platform and
  credential references, runtime-identity checks, and bounded migrations.
- Kept application storage separate from reusable development tooling, with
  small conditional routes and sanitized research, CI, and handoff evidence.

## Next

Validate a fresh marketplace installation from the public repository without
pre-existing local workspace conventions or provider-specific CI dependencies.
Use `docs/validation.md` for positive and negative activation scenarios; source
validation or an instruction walkthrough does not prove fresh-chat activation
or live platform permissions.

## Blockers

None.
