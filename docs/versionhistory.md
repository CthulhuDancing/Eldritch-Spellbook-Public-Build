# Version History

## 0.13.0 - Application data and workflow refinements

Added `application-data-and-secrets`, two conditional references, and behavioral
scenarios. Separated skill selection from action authorization, narrowed
handoffs to actual transfers, and refined workspace reuse, safe bootstrap,
and discoverable local-policy recording. Suitable task worktrees can be reused;
trivial edits need no full delivery flow unless required.

Consolidated repeated instructions and documentation, including the intermediate
0.12.1 routing work in this release. Preserved the eight skills, activation
settings, and permission/security boundaries.

## 0.12.0 - External code research

Added `external-code-research`, a read-only workflow for investigating public
upstream repositories and dependency internals. It uses the smallest available
authoritative source, treats external search as optional, verifies relevant
source before conclusions, and keeps external findings separate from local
repository discovery.

## 0.11.0 - Local workspace bootstrap

Added `local-workspace-bootstrap`, a narrowly triggered workflow for reusing
documented local tools, runtimes, caches, and worktree conventions before
creating replacements. It classifies environment failures, limits recovery to
targeted checks, records safe workspace-local guidance only with authorization,
and preserves project-local dependency ownership.

Routine worktree tasks now take a policy fast path when clear repository or
workspace guidance already exists. They avoid repeated instruction audits while
retaining concrete Git and target-path safety checks, and report whether local
conventions were reused, recorded, or not recorded.

## 0.10.0 - Portable CI failure recovery

Added `fix-ci`, an implicitly discoverable provider-neutral workflow for diagnosing failing builds, tests, linting, type checks, deployment checks, pull-request checks, and other automated validation. It identifies the earliest actionable root cause, distinguishes code defects from flaky or external failures before editing, applies the smallest safe correction when appropriate, and avoids weakening checks merely to obtain a green result.

## 0.9.0 - Portable discovery and handoffs

Replaced product-specific semantic-search guidance with `efficient-codebase-discovery`, a native-first workflow that uses exact search for known targets, progressively widens discovery for unfamiliar behavior, and may use semantic search only when an appropriate tool is already available. No external search service, API key, installation, or authentication is required.

Kept routine-worktree suitability discoverable so users do not need to know the skill name or exact workflow to request, while preserving its risk gate and user-controlled repository boundaries.

Expanded `agent-context-bridge` into two discoverable forward lanes: project handoffs for durable project continuation context and targeted task handoffs for one bounded Codex request. Preparing either handoff remains separate from invoking an agent or authorizing repository writes.

## 0.8.0 - Routine worktree task guidance

Added a gated workflow for deciding whether a narrow repository revision is suitable for an isolated-worktree task. It provides deterministic preparation, validation, draft-PR, and handoff guidance with clear escalation triggers while preserving project ownership and making no model-selection or runtime claims.

## 0.7.0 - Lean workflow refactor

Reduced the plugin to a small set of focused workflows, made consequential GitHub operations explicit-only, replaced formal handoff artifacts with a lightweight two-way context bridge, and collapsed active documentation around current status, durable decisions, and history.
