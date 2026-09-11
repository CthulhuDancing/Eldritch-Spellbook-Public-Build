---
name: routine-worktree-task
description: Prepare and deliver a bounded, low-risk repository change through an isolated worktree and draft PR when ownership and validation are clear. For trivial local edits, use only when isolated delivery is requested or required. Exclude unresolved architectural, production-sensitive, cross-repository, or secret-handling work.
---

# Routine Worktree Task

This is a repository delivery workflow, not authority to change models, task
creation, or agent runtime settings. Review and planning requests remain
read-only; perform delivery steps only within the user's authorized scope.

## Policy Fast Path

Reuse applicable instructions already in context. When worktree, branch,
review, and validation conventions are known, check only current Git state,
registered worktrees, and the exact target. Do not repeat instruction audits,
search alternate roots, or record unchanged policy.

If a required shared-resource convention needs setup or repair, use
local-workspace-bootstrap when available. Resolve single permission failures
through known guidance first; ordinary Git-state problems are not bootstrap
requests. Trivial local edits need no full delivery flow unless requested or
required by applicable guidance.

## Suitability

Proceed when one bounded change has clear ownership, maintained deterministic
validation, and fits one isolated branch/worktree and focused PR. No unresolved
architecture, product, or cross-repository decision, secret handling, or
material production change may remain.

If those conditions cease to hold, network/security behavior changes, or
validation fails unexpectedly, reassess outside the routine flow. Preserve
checkout and unrelated-change protections. For application storage or
credential concerns, use application-data-and-secrets when available.

## Delivery

1. Before editing, state or reuse the agreed scope, acceptance checks, ownership,
   base/branch, worktree, validation commands, and review focus. Inspect local and
   remote state and preserve unrelated work.
2. Reuse a suitable assistant-owned branch/worktree belonging to this task and
   meeting its requested base/isolation requirements. For a new task, fetch the
   requested or default base and create an isolated branch/worktree from it.
   Do not reuse another task's workspace, silently rebase approved work, alter
   the normal checkout, or write to the default branch without authorization
   for that action.
3. Read only missing or changed project context and make the scoped edits.
   Repository guidance owns runtime policy, dependencies, tests, CI, releases,
   and business behavior; keep shared tooling generic.
4. Run the complete required validation and record commands and results.
5. Commit and publish within the requested scope. A push request includes
   creating or updating a draft PR unless the user or applicable `AGENTS.md`
   explicitly excludes it.
   Do not merge, deploy, enable auto-merge, add reviewers, or add labels unless asked.
6. Report the branch/worktree, changed files, validation, PR reference, review
   risk, and `Local conventions: reused <source>`, `recorded <path>`, or
   `not recorded <reason>`.

Remove registered worktrees only through Git's worktree workflow when cleanup
is requested or included in the task; never manually delete their directories.
