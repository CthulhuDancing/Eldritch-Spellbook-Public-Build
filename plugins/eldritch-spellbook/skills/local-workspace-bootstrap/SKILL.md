---
name: local-workspace-bootstrap
description: Set up or repair reusable local development resources and user-selected workflow preferences, including worktree and push-to-PR conventions. Use for requested setup or a missing local choice that materially affects the current workflow; exclude routine work with sufficient policy, application storage, and ordinary project installs.
---

# Local Workspace Bootstrap

## Fast Path

Reuse applicable local policy and user choices already in context. Resolve only
the resource or preference needed now; do not audit the machine, reread unchanged
guidance, or recreate an equivalent resource.

This skill owns reusable development resources and local workflow preferences.
For application credentials
or persistent data, use application-data-and-secrets when available.

## Resolve Local Preferences

Keep reusable mechanics in skills and user-selected defaults in discoverable
local guidance. Enter this path for requested setup or when an unresolved
preference materially changes the next action; it is not an installation
questionnaire or a prerequisite for every task.

Reuse an established choice without asking again. Otherwise resolve only the
relevant choice and its scope (repository, workspace, or user). Use the scope
of the authorized instruction target when clear; ask if that remains material
and unresolved. For example:

| Preference | Choices to establish | When unset |
| --- | --- | --- |
| Push delivery | Push only, or also create/update a draft PR for the task branch | Push only; an explicit PR request still includes the PR |
| Worktree use | Isolate every repository edit, or reserve isolation for substantive work and requested branch/PR delivery | Follow repository requirements; trivial known-file edits need no full worktree workflow |

These are examples of local defaults, not a closed settings schema. Apply the
same path to another recurring development choice only when it affects the
requested work. Ask about a missing preference only if the answer is needed;
otherwise use the stated fallback and continue without blocking on setup.

A one-task choice is not a durable preference. Record it only when the user
asks to remember it or authorizes preference setup, using the recording steps
below without creating tool directories for preference-only setup. Record the
chosen behavior, scope, and any explicit standing authorization; do not infer
permission for unrelated publishing, merges, or production actions. A saved
push-to-draft-PR choice applies to future authorized pushes, not local edits.

Current explicit instructions can override a preference for one task without
rewriting it. Change a saved default only when requested. Revisit an established
choice only on a requested change or a concrete conflict, following the host's
instruction hierarchy.

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
host's instruction hierarchy, not a new precedence order. A current explicit
user request may update a stored preference while the host instruction
hierarchy still applies.

Reading or diagnosing does not authorize persistent setup. For authorized
bootstrap, apply only relevant steps without reconfirming safe steps within scope:

1. Prefer an existing safe shared workspace outside the repository. Otherwise,
   resolve a dedicated user-owned location outside source/release trees using
   the host filesystem. Check exact target, ownership, access, and contents;
   ask only if a material scope or ownership choice remains unresolved.
2. Create only needed resources. Do not imply authority to move installations,
   delete contents, widen permissions, or alter sandbox trust.
3. Record selected preferences or missing resource conventions in an authorized
   local instruction target, such as applicable local `AGENTS.md`. Include only
   needed locations, dependency ownership, or verification commands. Preserve
   existing guidance; keep personal defaults and machine topology out of tracked
   project files unless the user requests shared repository policy. Do not copy
   this skill or record credential values.
4. Make policy discoverable through the host's supported instruction entry
   point or a scoped pointer from applicable local guidance. A sibling
   `AGENTS.md` is not automatically loaded everywhere. Report any unrecorded
   pointer or discovery gap instead of promising future reuse. If no authorized
   target is available, use the choice for this task and report it as unsaved.

## Return

Report `Environment conventions: reused <source>`, `recorded <path>`, or
`not recorded <reason>`; the selected resources or preferences; any failure and sanitized
evidence; and recorded policy/pointer scope or remaining decision.
