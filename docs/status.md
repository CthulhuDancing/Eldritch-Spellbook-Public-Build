# Project Status

## Current

`0.14.0` refactors repository-oriented skills around evidence-driven workflow
gates, re-entry, and explicit stop conditions.

- `efficient-codebase-discovery` now owns both local and external code discovery
and includes a deterministic `map_repo.py` helper for first-pass repository
orientation when filesystem access is available.

- `fix-ci` and `routine-worktree-task` now use explicit evidence-driven loops to
avoid repeated equivalent actions when repository state or diagnostic evidence
has not changed.

- removed `external-code-research`. Rolled this functionality into `efficient-codebase-discovery`

## Next

Validate `0.14.0` through fresh marketplace installation and behavioral
scenarios, with particular attention to:

- `efficient-codebase-discovery` choosing correctly between known local targets,
  runtime-accessible repositories, remote-only repositories, and external
  upstream research;
- `map_repo.py` remaining useful across differently structured repositories
  without creating noisy classifications;
- CI and worktree flows stopping or reclassifying correctly when new evidence
  moves a task outside their intended scope.

Source validation and instruction walkthroughs do not prove fresh-install
activation, cross-platform execution, or actual service-account permissions.

## Blockers

None.