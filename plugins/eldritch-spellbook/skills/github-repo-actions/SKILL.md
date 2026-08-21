---
name: github-repo-actions
description: Perform explicit GitHub repository actions while preserving review boundaries. Use only when the user explicitly asks to inspect GitHub state or handle a branch, commit, push, issue, pull request, GitHub review, release, or cross-repository GitHub coordination. Do not use for ordinary local edits or inferred GitHub work.
---

# GitHub Repository Actions

Use GitHub state only to the depth required by the request. Keep verified facts separate from assumptions and report access gaps that affect confidence.

## Read actions

1. Resolve the repository and default branch.
2. Inspect only the requested issues, pull requests, reviews, releases, files, or overlapping work.
3. Summarize the requested state, material risks, and the smallest useful next action.

## Write actions

Treat the default branch as user-controlled. A general request to make or push a change authorizes a focused branch and pull request, not a direct default-branch write. Write directly to the default branch only when the user explicitly requests that exact path.

Before writing:

1. Confirm repository, remote, base branch, current branch, and working-tree state.
2. Preserve unrelated and user-owned changes.
3. Use an isolated assistant worktree when repository or workspace guidance requires it.
4. Create one focused branch and commit for one coherent review unit.
5. Run repository-relevant validation, push, and open or update the requested pull request.

Do not merge, enable auto-merge, request reviewers, assign users, add labels, close work, or create releases unless explicitly asked. For multi-repository work, keep branches, validation, and pull requests repository-local and state dependencies clearly.

Return a concise operational summary: GitHub state or action completed, branch/PR/release references when applicable, validation, unresolved risk, and next user decision.
