---
name: routine-worktree-task
description: Deliver bounded repository changes through an isolated branch and worktree when scope, ownership, validation, and review expectations are clear.
---

# Routine Worktree Task

Use this workflow for bounded, low-risk repository changes that fit one isolated
branch/worktree and have clear validation.

This workflow does not expand authority. Review and planning remain read-only;
delivery actions must stay within the user's authorized scope.

## Suitability Gate

Proceed only when:
- the requested change is bounded and clearly owned;
- the expected behavior is understood well enough to implement;
- maintained validation exists or success can be verified deterministically;
- the work fits one repository and one focused branch/worktree;
- no unresolved architectural, production-sensitive, cross-repository, or
  secret-handling decision remains.

If those conditions stop being true, leave the routine flow and reassess rather
than stretching the workflow to fit.

## Delivery Flow

1. Reuse established repository guidance, task scope, and local conventions.
   Inspect only the current Git state, registered worktrees, target files, and
   missing context needed for this change.

2. Establish the delivery state:
   - reuse a suitable assistant-owned branch/worktree for the same task when it
     still matches the requested base and isolation requirements;
   - otherwise create an isolated branch/worktree from the requested or default
     base;
   - preserve the normal checkout and unrelated work.

3. Confirm the implementation path before editing. If required behavior,
   ownership, or relevant source is still unclear, use the appropriate
   discovery workflow before continuing.

4. Make the smallest change that satisfies the agreed scope. Preserve unrelated
   behavior and follow repository-owned guidance for dependencies, runtime
   behavior, tests, CI, releases, and business rules.

5. Run the complete required validation.

6. If validation fails:
   - use the failure as new evidence;
   - determine whether it identifies a scoped defect in the current change;
   - if so, correct that defect and validate again;
   - if it instead exposes an architectural issue, production risk,
     cross-repository dependency, environment problem, permission boundary, or
     other condition outside this routine task, stop the loop and reassess.

7. Do not repeat an equivalent edit or validation attempt unless the repository
   state or available evidence materially changed.

8. When validation passes, commit and publish within the requested scope. A push
   request includes creating or updating a draft PR unless the user or
   applicable repository guidance explicitly excludes it.

9. Report the branch/worktree, changed files, validation performed, PR
   reference when applicable, remaining review risk, and relevant reused or
   recorded local conventions.

## Boundaries

Do not reuse another task's workspace, silently rebase approved work, alter the
normal checkout, or write to the default branch without authorization for that
action.

Do not merge, deploy, enable auto-merge, add reviewers, add labels, or perform
other consequential repository actions unless requested.

For application storage or credential concerns, use
application-data-and-secrets when available.

If a required shared-resource convention needs setup or repair, use
local-workspace-bootstrap when available. Ordinary Git-state problems do not
by themselves require bootstrap.

Remove registered worktrees only through Git's worktree workflow when cleanup
is requested or included in the task; never manually delete their directories.