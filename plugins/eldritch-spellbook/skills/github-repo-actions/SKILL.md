---
name: github-repo-actions
description: Handle explicitly requested GitHub inspection, branches, commits, pushes, issues, PRs, reviews, releases, or cross-repository coordination. Ordinary local edits do not imply GitHub work; the user need not name this skill.
---

# GitHub Repository Actions

Natural-language requests such as "open a PR" or "review this issue" select
this workflow, not permission for additional actions. Reviews remain read-only.
Local editing alone does not authorize publication.

## Read Actions

Resolve the repository and default branch, then inspect only the requested
state and relevant overlapping work. Separate verified facts from assumptions
and report access gaps that affect the answer.

## Write Actions

Treat the default branch as user-controlled: an authorized push or PR uses a
focused task branch unless the user explicitly requests a default-branch write.

1. Confirm repository, remote, base/current branch, and working-tree state.
   Preserve unrelated changes.
2. For repository edits, follow established branch/worktree conventions;
   use routine-worktree-task when available and suitable. Do not duplicate
   local-policy discovery here.
3. Group commits into coherent review units and run relevant validation.
   Commit and publish within the requested scope. A push request includes
   creating or updating a draft PR unless the user or applicable `AGENTS.md`
   explicitly excludes it.

Do not merge, deploy, enable auto-merge, request reviewers, assign users, add labels,
close work, or create releases unless explicitly asked. Keep multi-repository
branches, validation, and PRs repository-local and state their dependencies.

Return the inspected state or completed action, relevant references,
validation, unresolved risks, and any needed user decision.
