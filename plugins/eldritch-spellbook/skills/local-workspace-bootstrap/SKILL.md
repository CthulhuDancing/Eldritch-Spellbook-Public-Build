---
name: local-workspace-bootstrap
description: Reuse or safely establish local conventions for shared runtimes, tools, caches, and assistant worktrees. Use for explicit reusable-environment setup or repair, or before creating or replacing a shared resource when a required convention is missing, conflicting, or unusable. Do not use for ordinary project dependency installation, application data storage, or a single command failure that existing guidance already resolves.
---

# Local Workspace Bootstrap

Use existing local policy before creating a replacement runtime, tool, cache,
environment, or worktree convention. This workflow is for reusable local
environment setup and recovery, not ordinary project setup.

## Fast Path

Start from applicable instructions already available in the task. If they name
a usable shared runtime, tool directory, cache, worktree root, or escalation
path, reuse it. Verify only the specific path or command needed by the current
task; do not audit the machine, recreate an equivalent resource, or reread
guidance merely to confirm it exists.

## Failure Classification

Classify the earliest concrete failure before changing local state:

- **Sandbox or permission:** use the environment's authorized escalation path;
  do not create a replacement runtime or alter project configuration merely to
  bypass the boundary.
- **Missing executable or runtime:** check documented local locations and the
  active environment before proposing installation.
- **Missing project dependency:** follow the project's lockfile and setup
  process. Keep installed dependencies project-local; reuse a documented
  compatible download cache when available.
- **Cache, credential, network, or external-service failure:** report the
  boundary and use the documented recovery path. Do not substitute a new
  local service, credential, or package source.
- **Application or configuration defect:** return to the owning repository's
  normal diagnosis and validation workflow.

Do not repeat equivalent setup attempts without new evidence. Continue when
a targeted check reveals a different actionable cause; otherwise report the
boundary and the smallest needed decision. One failed command does not prove
that an installed resource is missing.

## Local Convention Resolution

Resolve ownership, not a new instruction hierarchy:

- Repository guidance owns project commands, dependencies, tests, and CI.
- Applicable workspace or machine `AGENTS.md` owns reusable local topology.
- Follow the host's instruction precedence; an explicit user change to a
  stored preference is not subordinate to that preference.
- Reading or diagnosing does not authorize persistent setup. An already
  authorized bootstrap needs no second confirmation for its safe, scoped steps.

Never put machine-specific paths, caches, ports, credentials, or local preview
steps into a project repository solely to solve a workstation concern.

When bootstrap is authorized, prefer an existing safe shared workspace outside
the repository. If none exists, resolve a dedicated user-owned location outside
source and release trees using the host's actual filesystem conventions.
Check the exact target, ownership, access, and existing contents before creating
only what is needed. Ask only if scope or ownership remains consequentially
unclear. Do not move existing installations, delete contents, widen permissions,
or alter sandbox trust as an implied part of bootstrap.

Record only missing durable conventions in an applicable local `AGENTS.md`:
the selected locations, compatibility and dependency-ownership rules, and any
needed verification or escalation command. Preserve user-authored guidance;
do not copy this skill or store credentials there.

Make the policy discoverable through the host's supported instruction entry
point, or a scoped pointer from already applicable local guidance. An
`AGENTS.md` in a sibling tooling folder is not automatically loaded by every
agent or workspace. Record the intended scope and pointer when authorized;
otherwise report the discovery gap instead of claiming future reuse is assured.

## Return

Report:

- `Environment conventions: reused <source>`, `recorded <path>`, or `not recorded <reason>`.
- the failure classification and sanitized evidence, when there was a failure.
- the runtime, tool, cache, or project setup path selected.
- any recorded policy/pointer, its scope, and the next decision if unresolved.
