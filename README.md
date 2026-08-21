# Eldritch Spellbook

A lean plugin for smoother, lower-overhead co-development with Codex.

The canonical plugin source is
[`plugins/eldritch-spellbook/`](plugins/eldritch-spellbook/). Repository agents
should begin with [`AGENTS.md`](AGENTS.md).

## Install from GitHub

Add this repository in the marketplace UI with:

- **Source:** `https://github.com/CthulhuDancing/Eldritch-Spellbook.git`
- **Git ref:** `main`
- **Sparse paths:** `.agents/plugins/marketplace.json` and `plugins/eldritch-spellbook`

Install the **Eldritch Spellbook** listing after the marketplace syncs.

## Skills

- [`efficient-codebase-discovery`](plugins/eldritch-spellbook/skills/efficient-codebase-discovery/) keeps unfamiliar-code discovery proportional, prefers exact native search when possible, and uses optional semantic search only when it is already available.
- [`github-repo-actions`](plugins/eldritch-spellbook/skills/github-repo-actions/) handles explicitly requested GitHub inspection and branch, commit, pull request, review, issue, or release actions.
- [`agent-context-bridge`](plugins/eldritch-spellbook/skills/agent-context-bridge/) recognizes when work should move between normal chat and a coding agent, using project handoffs for broader continuation context and targeted task handoffs for one bounded Codex request.
- [`routine-worktree-task`](plugins/eldritch-spellbook/skills/routine-worktree-task/) helps recognize and safely execute low-risk repository revisions through an isolated worktree and draft pull request.
- [`fix-ci`](plugins/eldritch-spellbook/skills/fix-ci/) implicitly diagnoses failing automated checks, separates code defects from CI/environment failures, and applies the smallest safe correction when appropriate.

The skills provide workflow guidance only. They do not install or authenticate
external services, invoke other agents, or silently change repository state.

## Maintenance

- [`docs/status.md`](docs/status.md) records the current resume point.
- [`docs/decisions.md`](docs/decisions.md) records durable design constraints.
- [`docs/versionhistory.md`](docs/versionhistory.md) records completed revisions.
