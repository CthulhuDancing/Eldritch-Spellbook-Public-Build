# Decisions

Record durable choices and their rationale here; procedures belong in skills.

## D001 - Canonical source

Edit `plugins/eldritch-spellbook/skills/<skill-name>`, not installed/cache copies,
so published behavior has one source of truth.

## D002 - Portable workflow focus

Public workflows must work without private repositories, machine-specific
layouts, personal skills, or a particular model. Local guidance supplies
actual workstation choices.

## D003 - Context budget

Keep the skill set small. Add a workflow or support file only when its distinct
trigger and reusable guidance justify the context and maintenance cost.

## D004 - Activation boundaries

Natural-language selection makes skills accessible without knowing their names.
Selection never authorizes unrequested actions; GitHub operations still need
the user's request for that action.

## D005 - Proportional discovery

Use known context and exact search first. Broader discovery is for unfamiliar
or unresolved behavior, not a repeated prerequisite for maintenance.

## D006 - User-controlled boundaries

Consequential actions, default-branch writes, merges, releases, and agent
invocation remain user-controlled rather than implied by workflow selection.

## D007 - Plugin distribution

Distribute the skills together as one `eldritch-spellbook` marketplace plugin,
avoiding separate installation and coordination requirements.

## D008 - Version format

Use pre-1.0 semantic versions: minor for meaningful workflow-family additions,
patch for compatible refinements.

## D009 - Routine worktree boundary

Routine delivery fits bounded work with clear ownership and deterministic
checks. It cannot resolve architectural/production risks or reconfigure
models. Projects retain ownership of commands, dependencies, tests, and releases.

## D010 - External tool independence

Optional search tools must improve discovery without becoming a required
service, installation, configuration, or authentication dependency.

## D011 - Handoff lanes

Project and targeted-task handoffs serve different context needs. Keep both,
sharing common fields without requiring broad history for a bounded task.
Actual transfer, not same-context implementation, triggers the workflow.

## D012 - CI recovery boundary

Separate code defects from environmental failures before editing. Passing
checks does not justify weakening validation without explicit authorization.

## D013 - Local workspace bootstrap boundary

Reuse documented compatible resources before replacement; keep project
dependencies project-local. Authorized setup may establish a safe user-owned
location and discoverable local policy. Fast-path reuse prevents repeated
audits; failure evidence, not fixed retry counts, governs recovery.

## D014 - External code research boundary

Public upstream implementation research is distinct from local discovery.
Keep it read-only and version-specific, separating verified source behavior
from inferred local implications.

## D015 - Application data and secrets boundary

Application storage and credentials need their own scope, not an always-on
security audit or shared-tooling bootstrap. Track portable contracts and safe
examples; keep local choices in discoverable local guidance and secret values
out of both.

Preserve actual-runtime access checks and controlled migration rollback:
directory names and Git ignores do not establish protection or remediate
leaks. Production cutover, rotation, destructive cleanup, and history changes
retain separate authorization.
