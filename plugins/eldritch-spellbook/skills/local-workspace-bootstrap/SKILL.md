---
name: local-workspace-bootstrap
description: Reuse or safely establish documented local workspace conventions for runtimes, tools, caches, and assistant worktrees. Use when the user explicitly asks to set up or repair reusable local workspace conventions, or when repeated equivalent sandbox, runtime-discovery, or dependency-bootstrap failures show that existing guidance cannot resolve them. Do not use for ordinary project dependency installation or one failed command.
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

Use one targeted verification and one appropriate recovery path. If the same
failure remains, stop repeating equivalent setup attempts and report the
evidence and needed user decision.

## Local Convention Resolution

Use this order for local conventions:

1. Repository instructions for project-owned behavior.
2. Existing workspace or machine-level `AGENTS.md` for local topology.
3. Current user instruction.
4. A confirmed shared workspace bootstrap, only when the current request
   authorizes persistent local setup.

Never put machine-specific paths, caches, ports, credentials, or local preview
steps into a project repository solely to solve a workstation concern.

When bootstrap is authorized, identify an existing multi-repository workspace
outside the current repository. If no safe shared workspace is evident, do not
invent a broad directory or create a worktree; ask the user to choose the
location.

In a confirmed workspace-level `AGENTS.md`, record only the missing local
conventions: shared tooling or runtime locations, cache policy, project-local
dependency ownership, assistant worktree location, escalation rule, and a
small verification command set. Preserve existing guidance and do not overwrite
user-authored content.

## Return

Report:

- `Environment conventions: reused <source>`, `recorded <path>`, or `not recorded <reason>`.
- the failure classification and exact evidence.
- the runtime, tool, cache, or project setup path selected.
- the next user decision when a safe local convention could not be established.
