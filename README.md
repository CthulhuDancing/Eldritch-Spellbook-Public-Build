# Eldritch Spellbook

A lean plugin for smoother, lower-overhead AI-assisted development workflows.

The canonical plugin source is
[`plugins/eldritch-spellbook/`](plugins/eldritch-spellbook/). Repository agents
should begin with [`AGENTS.md`](AGENTS.md).

## Install from GitHub

Add this repository in the marketplace UI with:

- **Source:** `https://github.com/CthulhuDancing/Eldritch-Spellbook-Public-Build.git`
- **Git ref:** `main`
- **Sparse paths:** `.agents/plugins/marketplace.json` and `plugins/eldritch-spellbook`

Install the **Eldritch Spellbook** listing after the marketplace syncs.

## Skills

- [`efficient-codebase-discovery`](plugins/eldritch-spellbook/skills/efficient-codebase-discovery/) keeps unfamiliar-code discovery proportional, prefers exact native search when possible, and uses optional semantic search only when it is already available.
- [`external-code-research`](plugins/eldritch-spellbook/skills/external-code-research/) investigates public upstream repositories or dependency internals when an external implementation detail matters, while keeping that work separate from local codebase discovery.
- [`local-workspace-bootstrap`](plugins/eldritch-spellbook/skills/local-workspace-bootstrap/) reuses documented local runtimes, tools, caches, and worktree conventions; it safely establishes those conventions only when its narrow bootstrap conditions apply.
- [`application-data-and-secrets`](plugins/eldritch-spellbook/skills/application-data-and-secrets/) separates portable configuration contracts from local credential and data storage, with scoped platform defaults, runtime-access checks, and safe migration boundaries.
- [`github-repo-actions`](plugins/eldritch-spellbook/skills/github-repo-actions/) handles explicitly requested GitHub inspection and branch, commit, pull request, review, issue, or release actions.
- [`agent-context-bridge`](plugins/eldritch-spellbook/skills/agent-context-bridge/) carries context when work actually transfers between conversations, tasks, or agents; it does not wrap ordinary implementation requests in handoff templates.
- [`routine-worktree-task`](plugins/eldritch-spellbook/skills/routine-worktree-task/) helps recognize and safely execute low-risk repository revisions through an isolated worktree and draft pull request.
- [`fix-ci`](plugins/eldritch-spellbook/skills/fix-ci/) implicitly diagnoses failing automated checks, separates code defects from CI/environment failures, and applies the smallest safe correction when appropriate.

The skills provide workflow guidance only. They do not install or authenticate
external services, invoke other agents, or silently change repository state.
Persistent local guidance is recorded only when the current request authorizes
the relevant setup and a safe local scope is established.

Plain-language requests can select the relevant skill without naming it.
Selection is separate from permission to act: reviews stay read-only, and local
edits do not imply publishing. Known local conventions take the fast path;
bootstrap fills only needed gaps and records how future tasks will find them.

Shared tooling and application storage have different owners: reuse compatible
development runtimes and caches, but do not accidentally share application
databases across workspaces or environments. The storage skill is conditional,
not an every-task security pass. It keeps platform details in two small
references and requires no personal skill, fixed directory, or new hosted service.

## Maintenance

- [`docs/status.md`](docs/status.md) records the current resume point.
- [`docs/decisions.md`](docs/decisions.md) records durable design constraints.
- [`docs/versionhistory.md`](docs/versionhistory.md) records completed revisions.
- [`docs/validation.md`](docs/validation.md) contains bounded behavioral checks for routing and storage changes.
