# Repository Agent Guide

Follow applicable host, workspace, and repository guidance. Keep work bounded
to the requested change, preserve unrelated edits, and do not modify other
repositories or local installations unless asked.

## Sources and Routing

- Canonical skills: `plugins/eldritch-spellbook/skills/<skill-name>/`.
  Installed/cache copies are outputs, not editing targets.
- Plugin metadata: `plugins/eldritch-spellbook/.codex-plugin/plugin.json`.
- Marketplace: `.agents/plugins/marketplace.json`.
- [README](README.md): installation and skill index.
- [Status](docs/status.md): current state and next verification.
- [Decisions](docs/decisions.md): durable choices and rationale.
- [Version history](docs/versionhistory.md): completed revisions.
- [Validation](docs/validation.md): behavioral scenarios.

Select relevant skills from their source descriptions; do not infer permission
from activation. For GitHub operations, read
`plugins/eldritch-spellbook/skills/github-repo-actions/SKILL.md`; apply
`routine-worktree-task` only when its suitability gate fits.

## Maintenance

Start from named files and the current diff. Expand discovery only for
unfamiliar, cross-cutting, or unresolved behavior.

Keep triggers narrow, bodies self-contained, and UI metadata aligned. Replace
overlapping instructions instead of appending caveats; explain net skill-word
growth in PRs. Update each document only for information it owns, without
copying workflow text into status or decisions.

Add support files only when actively used. Exclude placeholders, archives,
temporary output, and speculative scaffolding. Preserve existing activation,
dependency, and UI settings unless the task calls for changing them.

## Validation

There is no root build command. Validate changed skills and plugin metadata
with available validators; parse JSON/YAML, check relative links and stale
routing references, and run `git diff --check`. Match behavioral checks to the
change and report limitations. Do not require a particular local tool install.
