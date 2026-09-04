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
- [`github-repo-actions`](plugins/eldritch-spellbook/skills/github-repo-actions/) handles explicitly requested GitHub inspection and branch, commit, pull request, review, issue, or release actions.
- [`agent-context-bridge`](plugins/eldritch-spellbook/skills/agent-context-bridge/) recognizes when work should move between conversational and coding-agent workflows, using broader handoffs for continuation context and targeted task handoffs for bounded implementation work.
- [`routine-worktree-task`](plugins/eldritch-spellbook/skills/routine-worktree-task/) helps recognize and safely execute low-risk repository revisions through an isolated worktree and draft pull request.
- [`fix-ci`](plugins/eldritch-spellbook/skills/fix-ci/) implicitly diagnoses failing automated checks, separates code defects from CI/environment failures, and applies the smallest safe correction when appropriate.

The skills provide workflow guidance only. They do not install or authenticate
external services, invoke other agents, or silently change repository state.
Persistent local-workspace guidance is recorded only when the current request
authorizes bootstrap and a safe workspace scope is established.

## Maintenance

- [`docs/status.md`](docs/status.md) records the current resume point.
- [`docs/decisions.md`](docs/decisions.md) records durable design constraints.
- [`docs/versionhistory.md`](docs/versionhistory.md) records completed revisions.
