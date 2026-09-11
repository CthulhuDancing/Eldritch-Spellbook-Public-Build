---
name: fix-ci
description: Diagnose failing automated builds, tests, lint/type checks, deployment checks, PR checks, or pipelines, including reports that checks are red or broken. Use without assuming a particular CI provider; distinguish code defects from environmental failures before proposing or making corrections.
---

# Fix CI

Diagnose from evidence; failing automation alone does not authorize changes.

1. Start with the current branch/change and available failed checks, using an
   existing CI or repository integration. Do not require a provider, CLI, API,
   or service, or rediscover unrelated code.
2. Find the earliest actionable failure in the job, step, test, or log.
   Minimize captured output and redact secret values before sharing it.
3. Classify the cause:
   - **Code/configuration defect:** propose or, when authorized, fix the
     smallest relevant cause.
   - **Flaky/nondeterministic failure:** reproduce when practical; do not mask
     it with unrelated edits.
   - **Runner/infrastructure/external service:** report the boundary rather
     than changing application code to compensate.
   - **Permission/credential:** identify missing access without exposing or
     inventing credentials.
4. For authorized changes, preserve unrelated behavior and follow repository
   ownership and validation rules. Run the closest maintained local check
   before relying on remote CI alone.
5. Recheck automation when supported and authorized. Use new evidence if it
   remains red; do not repeat speculative edits. Stop when checks pass or the
   remaining failure is outside the code change, reporting cause, correction,
   validation, and unresolved blockers.

Do not weaken tests, delete checks, suppress errors, broaden ignores, or change
CI policy merely to get green unless the user explicitly requests that policy
change and the repository permits it. Commits, pushes, remote reruns, and other
mutations require current-request authorization; diagnosis can remain read-only.

Use application-data-and-secrets when available if the correction changes
application credential sources/storage or handles concrete exposure. A missing
runner credential alone needs scoped access diagnosis, not storage redesign.
