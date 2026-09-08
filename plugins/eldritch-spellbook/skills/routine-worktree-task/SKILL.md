---
name: routine-worktree-task
description: Recognize, prepare, and execute low-risk repository work through an isolated worktree and draft pull request. Use when a bounded change has clear ownership, deterministic validation, and no unresolved architectural, production-sensitive, cross-repository, or secret-handling concerns. For a trivial local edit, use only when isolated delivery is requested or required by applicable guidance. Decline the routine flow when its suitability conditions are not met.
---

# Routine Worktree Task

Keep this workflow advisory. It prepares a strong task brief and deterministic
delivery flow; it does not select or downgrade models, alter task-creation
defaults, or change Codex runtime configuration. Repository instructions
remain authoritative.

## Policy Fast Path

For a trivial local edit with no requested or required isolated-delivery flow,
follow normal local editing rules without a full worktree brief or PR workflow.

Start from applicable instructions already available in the current task. Do
not rediscover, reread, or audit every `AGENTS.md` merely to prove that local
conventions exist.

When known repository, workspace, or machine guidance clearly provides the
worktree location, branch and review rules, and relevant validation source,
reuse it. Perform only task-specific checks: current working-tree and remote
state, existing worktree registrations, and the exact target path. Do not
search for alternate workspace roots, repeat equivalent instruction reads, or
record local guidance.

Use local-workspace bootstrap when a required shared-resource convention must
be established or repaired before creating or replacing that resource. Resolve
a single permission failure through known guidance first; ordinary Git-state
problems do not call for environment bootstrap. A known convention never
replaces task-specific safety checks.

## Suitability Gate

Use this workflow only when every condition is true:

- The request is one bounded roadmap revision or similarly narrow change.
- Ownership and file boundaries are clear.
- No architecture or external product decision remains unresolved.
- No secret handling or material production behavior is involved.
- Maintained install, test, build, and/or validation commands exist.
- One isolated branch/worktree and focused pull request can contain the work.
- Deterministic checks and a concise review focus can express success.

If any condition is false, do not use the routine flow. Handle the request with
attention appropriate to the unresolved risk; preserve default-branch,
normal-checkout, and unrelated-change protections outside this flow too.

For review or planning, assess suitability without creating a worktree, editing,
committing, or publishing. Skill activation does not authorize delivery steps;
perform them only within the current request's scope.

## Task Brief

Before editing, state or confirm:

- **Scope:** named revision, acceptance condition, and excluded adjacent work.
- **Repository and ownership:** project-owned files and any shared boundary.
- **Base and branch:** current default branch and a focused task branch name.
- **Worktree:** reuse the documented location; if a shared convention is needed, resolve it through local-workspace bootstrap without assuming a fixed layout.
- **Local state:** normal checkout and existing worktrees inspected; unrelated
  local changes preserved.
- **Proof:** project-owned commands that demonstrate success.
- **Review focus:** the one or two risks a reviewer should inspect.

## Deterministic Workflow

1. Confirm scope, branch/base, worktree location, and preserved local changes.
2. Use applicable instructions and relevant project documentation; read only missing or changed context before editing.
3. Identify the project-owned install, test, build, and/or validation commands.
4. Reuse an existing assistant-owned branch/worktree when it belongs to this
   task and meets the requested base and isolation requirements; preserve its
   approved work. For a new task, fetch the requested or default base and create
   the isolated task branch/worktree from it. Do not reuse unrelated work,
   rebase an existing task silently, alter the normal checkout, or write to the
   default branch without authorization for that action.
5. Make only the requested changes. Keep shared tooling generic; leave project
   runtime policy, dependencies, tests, CI, release boundaries, and business
   behavior to the project.
6. Run the complete required validation and record exact commands and results.
7. When delivery is authorized, commit, push, and open a draft pull request. Do not merge, add reviewers or
   labels, or enable auto-merge unless the user explicitly asks.
8. Hand off the branch, worktree, changed files, validation, pull-request URL,
   review risk, and `Local conventions: reused <source>`, `recorded <path>`,
   or `not recorded <reason>`.

Do not manually delete a registered worktree. Remove one only through the
repository's Git worktree workflow when the user explicitly asks or cleanup is
part of the requested task.

## Escalate Out of Routine Flow

- Requirements conflict or lack a clear acceptance condition.
- An architectural boundary changes.
- Production, security, credential, or network behavior changes.
- Validation is missing, flaky, or fails unexpectedly.
- Scope expands beyond the named revision.
- Cross-repository ownership is uncertain.
