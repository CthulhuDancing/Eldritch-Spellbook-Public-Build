---
name: routine-worktree-task
description: Recognize, prepare, and execute low-risk repository work through an isolated worktree and draft pull request. Use when one bounded roadmap revision or similarly narrow request has clear ownership, deterministic validation, and no unresolved architectural, production-sensitive, cross-repository, or secret-handling concerns. Decline the routine flow when those conditions are not met.
---

# Routine Worktree Task

Keep this workflow advisory. It prepares a strong task brief and deterministic
delivery flow; it does not select or downgrade models, alter task-creation
defaults, or change Codex runtime configuration. Repository instructions
remain authoritative.

## Suitability Gate

Use this workflow only when every condition is true:

- The request is one bounded roadmap revision or similarly narrow change.
- Ownership and file boundaries are clear.
- No architecture or external product decision remains unresolved.
- No secret handling or material production behavior is involved.
- Maintained install, test, build, and/or validation commands exist.
- One isolated branch/worktree and focused pull request can contain the work.
- Deterministic checks and a concise review focus can express success.

If any condition is false, do not use the routine flow. Handle the request with the level of attention and user involvement appropriate to the unresolved risk.

## Task Brief

Before editing, state or confirm:

- **Scope:** named revision, acceptance condition, and excluded adjacent work.
- **Repository and ownership:** project-owned files and any shared boundary.
- **Base and branch:** current default branch and a focused task branch name.
- **Worktree:** an isolated location that follows repository or environment guidance when available; otherwise choose a safe local location without assuming a fixed directory layout.
- **Local state:** normal checkout and existing worktrees inspected; unrelated
  local changes preserved.
- **Proof:** project-owned commands that demonstrate success.
- **Review focus:** the one or two risks a reviewer should inspect.

## Deterministic Workflow

1. Confirm scope, branch/base, worktree location, and preserved local changes.
2. Read applicable repository instructions, roadmap or status documents, and component documentation before editing.
3. Identify the project-owned install, test, build, and/or validation commands.
4. Fetch the current default branch; create an isolated task branch and worktree from it, following repository and environment guidance when available.
5. Make only the requested changes. Keep shared tooling generic; leave project
   runtime policy, dependencies, tests, CI, release boundaries, and business
   behavior to the project.
6. Run the complete required validation and record exact commands and results.
7. Commit, push, and open a draft pull request. Do not merge, add reviewers or
   labels, or enable auto-merge unless the user explicitly asks.
8. Hand off the branch, worktree, changed files, validation, pull-request URL,
   and any specific review risk.

## Escalate Out of Routine Flow

- Requirements conflict or lack a clear acceptance condition.
- An architectural boundary changes.
- Production, security, credential, or network behavior changes.
- Validation is missing, flaky, or fails unexpectedly.
- Scope expands beyond the named revision.
- Cross-repository ownership is uncertain.
