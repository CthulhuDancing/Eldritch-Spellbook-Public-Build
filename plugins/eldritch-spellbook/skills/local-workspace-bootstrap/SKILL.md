---
name: local-workspace-bootstrap
description: Set up or repair reusable local runtimes, tools, caches, and worktree conventions, or resolve a required convention before creating or replacing a shared resource. Exclude application storage, ordinary project installs, and single failures that existing guidance resolves.
---

# Local Workspace Bootstrap

## Fast Path

Reuse applicable local policy already in context. Verify only the runtime,
tool, cache, worktree path, or escalation command needed now; do not audit the
machine, reread unchanged guidance, or recreate an equivalent resource.

This skill owns reusable development resources. For application credentials
or persistent data, use application-data-and-secrets when available.

## Diagnose Before Replacing

Classify the earliest concrete failure:

- **Sandbox/permission:** use the authorized escalation path, not a replacement
  runtime or project-configuration change that bypasses the boundary.
- **Missing executable/runtime:** check documented locations and the active
  environment before proposing installation.
- **Project dependency:** follow project setup and lockfiles. Keep installed
  dependencies project-local; reuse compatible documented download caches.
- **Cache, credential, network, or external service:** follow documented recovery
  or report the boundary; do not substitute services, credentials, or package sources.
- **Application/configuration defect:** return to repository diagnosis and validation.

One failed command does not prove a resource is missing. Retry only when new
evidence makes another check or recovery useful; otherwise report the cause
and smallest needed decision.

## Establish Only Missing Conventions

Repository guidance owns project commands, dependencies, tests, and CI;
applicable workspace or machine `AGENTS.md` owns reusable topology. Follow the
host's instruction hierarchy, not a new precedence order; explicit user
changes to stored preferences are not subordinate to those preferences.

Reading or diagnosing does not authorize persistent setup. For authorized
bootstrap, proceed without reconfirming safe steps within scope:

1. Prefer an existing safe shared workspace outside the repository. Otherwise,
   resolve a dedicated user-owned location outside source/release trees using
   the host filesystem. Check exact target, ownership, access, and contents;
   ask only if a material scope or ownership choice remains unresolved.
2. Create only needed resources. Do not imply authority to move installations,
   delete contents, widen permissions, or alter sandbox trust.
3. Record missing locations, compatibility/dependency-ownership rules, and
   needed verification or escalation commands in applicable local `AGENTS.md`.
   Preserve existing guidance; keep machine-specific topology out of tracked
   project files. Do not copy this skill or record credential values.
4. Make policy discoverable through the host's supported instruction entry
   point or a scoped pointer from applicable local guidance. A sibling
   `AGENTS.md` is not automatically loaded everywhere. Report any unrecorded
   pointer or discovery gap instead of promising future reuse.

## Return

Report `Environment conventions: reused <source>`, `recorded <path>`, or
`not recorded <reason>`; the selected resources; any failure and sanitized
evidence; and recorded policy/pointer scope or remaining decision.
