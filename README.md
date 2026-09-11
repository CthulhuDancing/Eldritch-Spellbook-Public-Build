# Eldritch Spellbook

A lean plugin for lower-overhead AI-assisted development.

## Install from GitHub

Add this repository in the marketplace UI:

- **Source:** `https://github.com/CthulhuDancing/Eldritch-Spellbook-Public-Build.git`
- **Git ref:** `main`
- **Sparse paths:** `.agents/plugins/marketplace.json` and `plugins/eldritch-spellbook`

After the marketplace syncs, install **Eldritch Spellbook**.

## Skills

- [`efficient-codebase-discovery`](plugins/eldritch-spellbook/skills/efficient-codebase-discovery/): locate unfamiliar behavior with native search and optional semantic tools.
- [`external-code-research`](plugins/eldritch-spellbook/skills/external-code-research/): investigate public upstream code and dependency internals.
- [`local-workspace-bootstrap`](plugins/eldritch-spellbook/skills/local-workspace-bootstrap/): reuse or safely establish shared development tools, caches, and worktree conventions.
- [`application-data-and-secrets`](plugins/eldritch-spellbook/skills/application-data-and-secrets/): scope application configuration, credentials, and persistent data.
- [`github-repo-actions`](plugins/eldritch-spellbook/skills/github-repo-actions/): handle requested GitHub inspection and publishing actions.
- [`agent-context-bridge`](plugins/eldritch-spellbook/skills/agent-context-bridge/): transfer project or task context between conversations and agents.
- [`routine-worktree-task`](plugins/eldritch-spellbook/skills/routine-worktree-task/): deliver bounded, low-risk changes through isolated worktrees and draft PRs.
- [`fix-ci`](plugins/eldritch-spellbook/skills/fix-ci/): distinguish code defects from environment failures and guide scoped corrections.

Plain-language requests select workflows, not permission for extra actions.
Established local policy takes the fast path; missing conventions are recorded
only within authorized setup. Shared tooling and application data remain
separate responsibilities. No personal skill, fixed machine layout, or new
hosted service is required.

## Maintenance

Canonical source is [`plugins/eldritch-spellbook/`](plugins/eldritch-spellbook/).
Repository contributors should start with [`AGENTS.md`](AGENTS.md).

- [Status](docs/status.md): current state and next steps.
- [Decisions](docs/decisions.md): design rationale.
- [Version history](docs/versionhistory.md): completed revisions.
- [Validation](docs/validation.md): routing and storage scenarios.
