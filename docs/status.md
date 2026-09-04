# Project Status

## Version

`0.12.0` - External code research

## Current phase

Validate the seven-skill plugin from its public repository.

## Completed

- Replaced Morph-specific discovery guidance with a native-first, tool-optional workflow.
- Kept codebase discovery implicit for unfamiliar or scattered behavior while preferring exact native search for known targets.
- Kept routine-worktree suitability discoverable for users who may not know which workflow to request.
- Made agent handoff preparation discoverable and split it into project and targeted-task lanes.
- Kept GitHub repository actions explicit-only.
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

## Next

Validate a fresh marketplace installation from the public repository without
pre-existing local workspace conventions or provider-specific CI dependencies.

## Blockers

None.
