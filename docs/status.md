# Project Status

## Current

`0.16.0` adds local workflow-preference setup to bootstrap, with saved worktree
and push-delivery choices reused by delivery skills. Unconfigured pushes remain
push-only. The plugin still contains eight workflows, including `test-design`
from `0.15.0`. Marketplace installation has not been verified.

The preceding `0.14.0` release established:

- `efficient-codebase-discovery` now owns both local and external code discovery
and includes a deterministic `map_repo.py` helper for first-pass repository
orientation when filesystem access is available.

- `fix-ci` and `routine-worktree-task` now use explicit evidence-driven loops to
avoid repeated equivalent actions when repository state or diagnostic evidence
has not changed.

- Removed `external-code-research` and folded its functionality into `efficient-codebase-discovery`.

## Next

Validate `0.16.0` through fresh marketplace installation and behavioral
scenarios, including the outstanding earlier checks:

- local preferences being recorded only during authorized setup, discovered in
  a new task, reused without prompting, and overridden for one task;
- unconfigured pushes and trivial edits proceeding without mandatory setup;

- `test-design` reusing sufficient coverage, selecting contract-based
regressions, rejecting speculative cases, and justifying no-test decisions;

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
