---
name: fix-ci
description: Diagnose failing automated builds, tests, lint/type checks, deployment checks, PR checks, or pipelines, including reports that checks are red or broken. Use without assuming a particular CI provider; distinguish code defects from environmental failures before proposing or making corrections.
---

# Fix CI

Diagnose from evidence; failing automation alone does not authorize code changes.

## Diagnostic Flow

1. Start with the current branch/change and available failed checks, using an
   existing CI or repository integration. Do not require a provider, CLI, API,
   or service.

2. Find the earliest actionable failure in the job, step, test, or log.
   Minimize captured output and redact secret values before sharing it. Do not rediscover unrelated code.

3. Classify the failure:
   - **Code/configuration defect:** propose or, when authorized, correct the
     smallest relevant cause.
   - **Flaky/nondeterministic failure:** reproduce when practical before
     editing; do not mask it with unrelated changes.
   - **Runner/infrastructure/external service:** report the external boundary
     rather than changing application code to compensate.
   - **Permission/credential:** identify missing access without exposing or
     inventing credentials.

4. For authorized corrections, preserve unrelated behavior and follow
   repository ownership and validation rules. Run the closest maintained local
   check before relying on remote CI alone.

5. After a correction or meaningful reproduction attempt, recheck the relevant
   validation or automation when supported and authorized.

6. If validation still fails:
   - treat the new failure as evidence;
   - reclassify only when the evidence materially changes the diagnosis;
   - take another corrective or diagnostic action only when the new evidence
     supports it.

7. Do not repeat an equivalent edit, rerun, reproduction attempt, or diagnostic
   action unless the state or available evidence materially changed.

8. Stop when checks pass, the remaining failure is outside the code change, or
   another iteration would not make evidence-driven progress. Report the cause,
   correction or diagnosis, validation performed, and unresolved blockers.

## Boundaries

Do not weaken tests, delete checks, suppress errors, broaden ignores, or change
CI policy merely to get green unless the user explicitly requests that policy
change and the repository permits it.

Commits, pushes, remote reruns, and other mutations require current-request
authorization; diagnosis can remain read-only.

Use application-data-and-secrets when available if the correction changes
application credential sources/storage or handles concrete exposure. A missing
runner credential alone needs scoped access diagnosis, not storage redesign.