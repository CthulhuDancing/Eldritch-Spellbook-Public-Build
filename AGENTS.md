# Repository Agent Guide

These instructions apply to the entire repository. Also follow any applicable repository- or workspace-level guidance that is available in the current environment.

## Working approach

- Make bounded edits directly from the current request, named files, and current diff.
- Do not rediscover the whole repository for ordinary maintenance. Expand discovery only when the change is unfamiliar, cross-cutting, or blocked by missing evidence.
- Preserve unrelated and user-owned changes.
- Keep edits inside this repository unless the user explicitly requests changes elsewhere.
- Use a skill only when its trigger applies. Explicit-only skills must never be inferred from nearby work.

For explicit GitHub operations, use
`plugins/eldritch-spellbook/skills/github-repo-actions/SKILL.md`.
Use `plugins/eldritch-spellbook/skills/agent-context-bridge/SKILL.md` when project context or a bounded task should be handed between normal chat and a coding agent.
Use `plugins/eldritch-spellbook/skills/routine-worktree-task/SKILL.md` when a bounded, low-risk repository revision fits its suitability gate.
Use `plugins/eldritch-spellbook/skills/local-workspace-bootstrap/SKILL.md` only when the user asks to establish or repair reusable local workspace conventions, or repeated equivalent environment failures show that documented local policy is missing.
Use `plugins/eldritch-spellbook/skills/fix-ci/SKILL.md` when automated checks are failing or reported as red/broken, including when the user does not know the CI provider or terminology.
Use `efficient-codebase-discovery` for unfamiliar or scattered code discovery; use exact search and targeted reads for known paths, symbols, strings, errors, or patterns.

## Repository layout

- `.agents/plugins/marketplace.json` exposes the local marketplace entry.
- `plugins/eldritch-spellbook/.codex-plugin/plugin.json` owns plugin metadata.
- `plugins/eldritch-spellbook/skills/<skill-name>/` contains canonical skill sources.
- `README.md` is human-facing navigation.
- `docs/status.md` is the current resume point.
- `docs/decisions.md` records durable constraints.
- `docs/versionhistory.md` records completed revisions.

Add directories and support files only when the plugin actively uses them. Do
not commit placeholders, generated archives, temporary output, or speculative
scaffolding.

## Skill and plugin changes

- Keep trigger descriptions narrow and bodies concise; every installed skill consumes discoverability and context budget.
- Keep `agents/openai.yaml` aligned with its `SKILL.md` and reserve explicit-only activation for workflows that truly require deliberate user intent.
- Use available skill or plugin validators when the environment provides them; do not assume a particular shared tool or local installation exists.
- Update status, decisions, or version history only when their owned information changes.

## Validation

This repository has no root build command. Match checks to the change:

- Validate changed skills and plugin metadata with available validators when present.
- Parse changed JSON and YAML with structured tools.
- Search active guidance for stale paths or removed skill names.
- Inspect the final diff and report any validation that could not run.
