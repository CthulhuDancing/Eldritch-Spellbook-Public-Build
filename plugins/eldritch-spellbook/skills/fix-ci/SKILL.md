---
name: fix-ci
description: Diagnose and resolve failing automated checks for a code change. Use implicitly when builds, tests, linting, type checks, deployment checks, pull-request checks, or CI pipelines are failing or reported as red/broken, including when the user does not know the CI provider or terminology. Inspect available check output, identify the first actionable root cause, make the smallest safe correction when appropriate, validate locally when possible, and distinguish code defects from flaky, infrastructure, permission, or external-service failures.
---

# Fix CI

Treat failing automation as evidence to diagnose, not as a command to change code blindly.

1. Start from the current branch, change, task, or pull request and the available failed checks. Do not rediscover unrelated repository structure.
2. Use the CI or repository integration already available in the environment. Do not require a particular provider, CLI, API, or hosted service.
3. Read the failing job, step, test, or log closely enough to identify the earliest actionable root cause. Prefer the first meaningful failure over downstream noise. Minimize captured output and redact secret values before sharing diagnostics.
4. Classify the failure before editing:
   - **Code/configuration defect:** fix the smallest relevant cause.
   - **Flaky or nondeterministic failure:** reproduce when practical; do not mask it with unrelated code changes.
   - **Runner/infrastructure/external-service failure:** report the blocker and avoid changing application code merely to make a broken environment pass.
   - **Permission/credential/secret failure:** identify the missing boundary without exposing or inventing credentials.
5. If code changes are appropriate, preserve existing behavior outside the failure and follow repository-specific instructions, ownership boundaries, and validation commands.
6. Run the closest relevant local test, lint, type-check, build, or other maintained validation before relying on remote CI alone.
7. Re-check the failed automation when the environment supports it. If it remains red, use the new evidence rather than repeating the same search or speculative edits.
8. Stop when checks pass or when the remaining failure is clearly outside the code change. Report the root cause, correction, validation, and any unresolved external blocker concisely.

Do not weaken tests, delete checks, suppress errors, broaden ignores, or alter CI policy merely to obtain a green result unless the user explicitly requests that policy change and the repository permits it.

Do not create commits, push branches, rerun remote jobs, or mutate repository state unless the current request and applicable repository workflow authorize those actions. Diagnosis and a proposed fix can still proceed when write access or CI-control actions are unavailable.

Use application-data-and-secrets when available only if the correction changes
application credential sources or storage, or a concrete exposure needs
handling. A missing CI credential alone needs a scoped access diagnosis, not
an application-storage redesign.
