---
name: application-data-and-secrets
description: Set up, change, or explicitly review how an application obtains credentials and deployment configuration or stores persistent/private data, logs, and caches. Use for credential-source integration, application storage paths, and data/configuration migrations. Do not turn unrelated code edits, ordinary dependency setup, or a missing CI credential into a general security audit.
---

# Application Data and Secrets

Keep portable application contracts in source, actual local choices in
applicable local guidance, and sensitive values out of both. This skill owns
application storage and credential handling, not shared development tooling
or a comprehensive security review.

## Policy Fast Path

Use relevant instructions and evidence already in context. Reuse policy for
the paths, credential sources, and runtime identities relevant to the task;
resolve only needed gaps and verify the touched contract and access. Do not inventory the machine,
reread every `AGENTS.md`, or migrate working conventions merely to match an
example. Investigate concrete conflicts or unsafe exposure, not hypothetical
gaps unrelated to the task.

## Scoped Workflow

Apply only relevant steps; a storage-only change does not need a credential audit.

1. **Confirm the boundary.** Distinguish review, setup, and migration. A review
   is read-only. Existing authorization covers safe steps within its scope;
   ask only about material unresolved access, ownership, or operational choices.
2. **Identify the contract.** Inspect the relevant configuration loader,
   variable names, path resolution, and runtime account without dumping
   credentials or private data. Separate portable defaults/templates from
   deployment configuration, secrets, durable data, logs, and disposable cache.
3. **Choose or reuse storage.** Keep live credentials, machine-specific
   deployment configuration, and persistent/private runtime data outside
   tracked source and release trees. Track safe schemas and placeholders such
   as `.env.example`; `.env` is a format, not a security boundary. For a new or
   changed directory decision, read [storage locations](references/storage-locations.md).
   Scope mutable data by application and environment, and by instance when
   parallel workspaces must not share state. Create only needed directories.
4. **Handle credentials.** Prefer a supported existing identity or secret
   facility; do not require a new service, subscription, or personal skill.
   Before integrating, moving, or responding to exposed credentials, read
   [credential handling](references/credential-handling.md). Never put values
   in prompts, `AGENTS.md`, commits, logs, or handoffs. Report names/references
   and sanitized diagnostics instead.
5. **Change and verify proportionately.** Follow the repository's isolated
   branch and review rules even when secret-related work is not routine.
   Check loader precedence, resolved paths, and necessary access under the
   actual runtime identity when possible; an administrator's successful read
   is not proof of service access. Do not widen permissions or bypass a sandbox
   merely to pass a check.

For an authorized migration, first resolve exact source/destination, access,
active writers, and rollback. Preserve a protected recoverable copy; validate
the application's load/write behavior before cutover or cleanup. Do not move
live production data, delete originals, rotate credentials, or rewrite history
by inference. Report any untested runtime identity or cutover step explicitly.

## Local Conventions and Return

For authorized local setup, record only missing durable choices in an
applicable local `AGENTS.md` or its referenced local document: app/environment
scope, needed roots, credential source names, runtime identity/access, and
verification. Keep machine topology out of tracked project guidance. Preserve
existing content and use the host's instruction precedence.

Ensure later tasks can find that policy through a supported instruction entry
point or a scoped pointer from already applicable local guidance. Do not assume
a sibling file is loaded. If recording is outside authorized scope, report
the gap. Use local-workspace bootstrap only if shared development conventions
also need setup or repair; application storage alone does not trigger it.

Return the decision/change, validation and remaining risk, plus
`Local conventions: reused <source>`, `recorded <path and scope>`, or
`not recorded <reason>`. Include any changed discovery pointer, never values.
