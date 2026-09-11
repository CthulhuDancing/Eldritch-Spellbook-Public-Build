---
name: application-data-and-secrets
description: Set up, change, migrate, or explicitly review application credential sources, deployment-configuration storage, and persistent/private data, logs, or caches. Exclude unrelated edits, development-tool bootstrap, and ordinary missing CI credentials; this is not a general security audit.
---

# Application Data and Secrets

Keep portable contracts in source, actual local choices in applicable guidance,
and secret values in neither.

## Policy Fast Path

Reuse relevant policy and evidence already in context; resolve only needed gaps
and verify the touched contract/access. Do not inventory the machine, reread
every `AGENTS.md`, or migrate safe conventions to match an example. Investigate
concrete conflicts or exposure, not unrelated hypothetical gaps.

## Workflow

Apply only relevant steps; storage-only changes need no credential audit.

1. Distinguish review, setup, and migration. Reviews/plans are read-only;
   existing authorization covers safe steps within scope. Ask only about
   material unresolved access, ownership, or operational choices.
2. Inspect relevant configuration loaders, variable names, path resolution,
   and runtime identity without dumping credentials or private data. Separate
   portable defaults/templates from deployment configuration, secrets, durable
   data, logs, and disposable cache.
3. Keep live credentials, machine-specific deployment configuration, and
   persistent/private runtime data outside tracked source and release trees.
   Track safe schemas and placeholders such as `.env.example`; the `.env`
   format itself provides no protection. For directory decisions, read
   [storage locations](references/storage-locations.md). Scope mutable data by
   application/environment and, when workspaces must not share state, instance.
   Create only needed directories.
4. Before integrating, moving, or responding to exposed credentials, read
   [credential handling](references/credential-handling.md). Prefer supported
   existing identity/secret facilities; require no new service, subscription,
   or personal skill. Keep values out of prompts, `AGENTS.md`, commits, logs,
   and handoffs; report names/references and sanitized evidence.
5. Follow repository branch/review rules even when the work is not routine.
   Check loader precedence, resolved paths, and required access under the
   actual runtime identity where possible. An administrator's read is not
   proof of service access. Do not widen permissions or bypass a sandbox
   merely to pass verification.

For an authorized migration, resolve exact source/destination, access, active
writers, and rollback first. Preserve a protected recoverable copy and verify
application load/write behavior before cutover or cleanup. Do not infer
permission for live production moves, deleting originals, rotation, or history
rewrites. Report untested identity checks and cutover steps.

## Local Conventions and Return

During authorized local setup, record only missing app/environment scope,
needed roots, credential source names, runtime identity/access, and verification
in applicable local `AGENTS.md` or its referenced document. Preserve existing
content and host instruction precedence; keep machine topology out of tracked
project guidance.

Use a supported instruction entry point or scoped pointer so future tasks can
find the policy; a sibling file alone is insufficient. If no authorized local
instruction target exists, report the discovery gap or recording need instead
of writing anything outside the authorized scope. Shared development setup
belongs to local-workspace-bootstrap when available, not this workflow.

Return the decision/change, validation, remaining risk, and
`Local conventions: reused <source>`, `recorded <path and scope>`, or
`not recorded <reason>`. Include changed discovery pointers, never values.
