# Decisions

Record only durable choices that future work must preserve.

## D001 - Canonical source

Canonical skill source lives in
`plugins/eldritch-spellbook/skills/<skill-name>`. Installed and cached copies
are outputs, not editing targets.

## D002 - Portable workflow focus

The plugin provides reusable co-development workflows without assuming a specific machine, workspace layout, shared tool installation, or private repository environment.

## D003 - Context budget

Keep the installable skill set small, trigger descriptions narrow, and skill
bodies concise. Add a skill only when repeated use proves that its dedicated
trigger and instructions save more effort than they consume.

## D004 - Activation boundaries

Skills may be selected automatically when their narrow descriptions fit.
GitHub actions require an explicit user request for the action, not an explicit
skill-name invocation. Skill selection never supplies permission for writes,
publishing, or coordination; read-only requests remain read-only.

## D005 - Proportional discovery

Bounded follow-ups start from the current conversation, named targets, and
current diff. Broader discovery is reserved for unfamiliar, cross-cutting, or
genuinely unresolved work. Prefer exact native search for known targets and use semantic search only when an already-available tool materially reduces exploration.

## D006 - User-controlled boundaries

The user owns consequential decisions, default-branch writes, merges, releases,
and agent invocation. Skills may prepare work but do not silently cross those
boundaries.

## D007 - Plugin distribution

Distribute the skills together through the repository marketplace as one
`eldritch-spellbook` plugin.

## D008 - Version format

Use pre-1.0 semantic versions. Increment the minor version for a meaningful
workflow-family change and the patch version for compatible refinements.

## D009 - Routine worktree boundary

Routine-worktree guidance may be discovered implicitly but remains advisory and gated. It may determine whether a narrow repository request has deterministic delivery conditions and prepare a worktree brief and workflow, but it must not select or downgrade a model, alter task-creation defaults, or change Codex runtime configuration. Project instructions remain authoritative for runtime policy, dependencies, validation, CI, release boundaries, and business behavior.

## D010 - External tool independence

No installable workflow may require Morph or another external semantic-search service. Optional external search tools may be used only when already available and helpful; skills must not install, configure, authenticate, or depend on them.

## D011 - Handoff lanes

Agent handoff preparation uses two forward lanes. Project handoffs carry durable project state, decisions, constraints, and open work when a coding agent needs broad continuation context. Targeted task handoffs carry only the minimum context needed for one bounded implementation, fix, investigation, refactor, or review. Both may be discovered implicitly for an actual transfer between tasks, agents, or environments, not ordinary implementation in the current context. Preparing a handoff does not itself authorize agent invocation or repository writes.

## D012 - CI recovery boundary

`fix-ci` is provider-neutral and may be discovered implicitly from failing builds, tests, linting, type checks, deployment checks, pull-request checks, or other automated validation. It must distinguish code defects from flaky, infrastructure, permission, credential, and external-service failures before editing. A green result does not justify weakening tests, suppressing errors, broadening ignores, or changing CI policy without explicit user direction.

## D013 - Local workspace bootstrap boundary

`local-workspace-bootstrap` reuses documented local runtimes, tools, caches,
and worktree conventions before attempting any replacement. It applies to
explicit reusable-environment setup or repair, or an unresolved required
convention before shared-resource creation or replacement. Known recovery
guidance and ordinary project installs do not need a full bootstrap.

Persistent setup requires current-request authorization. A safe, dedicated
user-owned location may be established when no shared workspace exists. Record
only missing conventions in applicable local guidance and make discovery
explicit through a supported entry point or scoped pointer; a sibling
`AGENTS.md` alone is insufficient. Machine topology stays out of tracked project
guidance. Ownership rules do not override the host's instruction hierarchy.
Project dependencies remain project-local; compatible caches and runtimes may
be reused. Retry only when new evidence makes the next step useful.

## D014 - External code research boundary

`external-code-research` covers public upstream repositories and dependency
internals, not the current repository. It uses the smallest available
authoritative source, treats external search tools as optional, and verifies
relevant source before drawing conclusions. It remains read-only and reports
the source revision, relevant files, and any inference separately from verified
facts.

## D015 - Application data and secrets boundary

`application-data-and-secrets` owns application credential sources,
deployment-configuration storage, and persistent/private data locations.
It is not an always-on security audit or shared-tooling bootstrap. Existing
safe policy takes a task-specific fast path; platform and credential details
load only for their relevant decisions.

Track portable contracts and safe examples. Record actual machine choices in
discoverable, applicable local guidance only within authorized setup; never
record secret values. Prefer existing supported identity/secret facilities
without adding a provider dependency. Directory names and Git ignores do not
prove access control or remediate leaks. Validate the runtime identity and
preserve controlled rollback for authorized migrations. Production cutover,
credential revocation, destructive cleanup, and history changes retain their
own authorization boundaries.
