# Project Status

## Version

`0.10.0` - Portable CI failure recovery

## Current phase

Prepare the portable five-skill plugin for a clean public repository.

## Completed

- Replaced Morph-specific discovery guidance with a native-first, tool-optional workflow.
- Kept codebase discovery implicit for unfamiliar or scattered behavior while preferring exact native search for known targets.
- Kept routine-worktree suitability discoverable for users who may not know which workflow to request.
- Made agent handoff preparation discoverable and split it into project and targeted-task lanes.
- Kept GitHub repository actions explicit-only.
- Added provider-neutral `fix-ci` guidance that implicitly diagnoses failing automated checks and separates code defects from environment or external failures.
- Removed machine-specific paths, fixed worktree locations, and shared-tooling assumptions.
- Preserved user-controlled boundaries for consequential GitHub and agent actions.
- Merged the portability and workflow cleanup into `main`.

## Next

Copy the clean current tree into a new public repository with fresh Git history, then validate a fresh marketplace installation without Morph credentials, private workspace tooling, or provider-specific CI dependencies.

## Blockers

None.
