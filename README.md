# Eldritch Spellbook

Find relevant code, diagnose failed checks, preserve work, and hand off context
with eight focused development workflows.

For developers who want agents to reuse local conventions and make proportionate,
evidence-based decisions. The workflows adapt to repository guidance without
requiring a new hosted service or tool stack.

Try requests such as:

- "Find where this behavior is implemented."
- "Fix the failed check and reuse existing regression coverage where sufficient."
- "Set up my local preferences: isolate repository edits and include a draft PR
  when I ask you to push."

## Install from GitHub

Add this repository in the marketplace UI:

- **Source:** `https://github.com/CthulhuDancing/Eldritch-Spellbook-Public-Build.git`
- **Git ref:** `main`
- **Sparse paths:** `.agents/plugins/marketplace.json` and `plugins/eldritch-spellbook`

After the marketplace syncs, install **Eldritch Spellbook**.

## Skills

- [`efficient-codebase-discovery`](plugins/eldritch-spellbook/skills/efficient-codebase-discovery/): locate local or upstream implementation behavior with deterministic repository mapping, targeted search, and evidence-driven source inspection.
- [`local-workspace-bootstrap`](plugins/eldritch-spellbook/skills/local-workspace-bootstrap/): establish reusable tools and locally saved preferences for worktrees, push delivery, and other relevant development choices.
- [`application-data-and-secrets`](plugins/eldritch-spellbook/skills/application-data-and-secrets/): scope application configuration, credentials, and persistent data.
- [`github-repo-actions`](plugins/eldritch-spellbook/skills/github-repo-actions/): handle requested GitHub inspection and publishing actions.
- [`agent-context-bridge`](plugins/eldritch-spellbook/skills/agent-context-bridge/): transfer project or task context between conversations and agents.
- [`routine-worktree-task`](plugins/eldritch-spellbook/skills/routine-worktree-task/): deliver bounded, low-risk changes through isolated worktrees and draft PRs.
- [`fix-ci`](plugins/eldritch-spellbook/skills/fix-ci/): distinguish code defects from environment failures and guide scoped corrections.
- [`test-design`](plugins/eldritch-spellbook/skills/test-design/): inspect existing coverage and justify behavioral tests without speculative suite growth.

Plain-language requests select workflows, not permission for extra actions.
Established local policy takes the fast path; missing conventions are recorded
only within authorized setup. Shared tooling and application data remain
separate responsibilities. No personal skill, fixed machine layout, or new
hosted service is required.

## Local preferences

Bootstrap can record user-selected defaults once in authorized, discoverable
local guidance. Existing choices are reused; missing preferences do not require
a setup questionnaire before ordinary work. Preferences stay local unless you
ask to make them shared repository policy.

Without a saved push-to-PR preference, "push" only pushes; "open a PR" includes
the PR. Trivial known-file edits avoid the full worktree workflow unless local
policy or a branch/PR request requires it. You can override a default for one
task without changing the saved preference. Setup does not change installations
or grant permission for unrelated actions.

## Maintenance

Canonical source is [`plugins/eldritch-spellbook/`](plugins/eldritch-spellbook/).
Repository contributors should start with [`AGENTS.md`](AGENTS.md).

- [Status](docs/status.md): current state and next steps.
- [Decisions](docs/decisions.md): design rationale.
- [Version history](docs/versionhistory.md): completed revisions.
- [Validation](docs/validation.md): routing and storage scenarios.
