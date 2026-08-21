---
name: agent-context-bridge
description: Prepare compact handoffs between normal chat and Codex or another coding agent. Use implicitly when a conversation has enough project or task context that moving implementation to a coding agent would be useful, when the user asks Codex to take over or implement something, or when completed agent work needs to be translated back into normal chat. Choose a project handoff for broad continuation context and a targeted task handoff for one bounded implementation request. Do not invoke another agent or start implementation unless the current environment and user request explicitly support that action.
---

# Agent Context Bridge

Move only the context that improves the next agent's work. Prefer confirmed conversation state and named artifacts; inspect repository state only when needed to make the handoff accurate.

## Choose a Forward Lane

### Project Handoff

Use when Codex needs enough durable context to continue a project or substantial workstream across multiple tasks.

Produce compact Markdown with:

- **Project goal:** the larger outcome being pursued.
- **Current state:** confirmed implementation state and completed work.
- **Decisions:** durable choices the coding agent must preserve.
- **Constraints:** compatibility, safety, scope, and explicit exclusions.
- **Repository orientation:** only the important files, components, branches, or documentation already known to matter.
- **Open work:** prioritized remaining work or the immediate next objective.
- **Validation:** project-owned checks that matter when changes are made.
- **Completion report:** what Codex should return to normal chat.

Keep historical narrative out unless it explains a current constraint or decision. Do not make Codex rediscover information already established in chat.

### Targeted Task Handoff

Use for one specific implementation, fix, investigation, refactor, or review task that Codex can execute without carrying the whole project conversation.

Produce a focused prompt with:

- **Task:** one concrete outcome.
- **Relevant context:** only facts needed to perform this task correctly.
- **Scope:** named files or components when known, plus adjacent work that must remain untouched.
- **Constraints:** compatibility, safety, preserved behavior, and user decisions.
- **Acceptance checks:** observable conditions that define success.
- **Validation:** known project-owned commands or checks when relevant.
- **Return:** the concise completion information needed back in normal chat.

Do not include broad project history, speculative file lists, or decisions unrelated to the task. Prefer a short executable brief over a comprehensive summary.

## Codex or Task Agent to Chat

When completed agent work is being returned to normal chat, produce compact Markdown with:

- **Changed:** completed behavior and important implementation choices.
- **Verified:** checks run and their results.
- **Open risks:** gaps, failures, or `None`.
- **References:** relevant files, task, branch, pull request, or issue links.
- **Next decision:** the smallest useful choice or follow-up for normal chat.

## Boundaries

Do not manufacture decisions or hide material uncertainty in assumptions. State unresolved questions only when they actually block or materially change the work.

Preparing a handoff does not itself authorize repository writes, agent invocation, merges, releases, or other consequential actions. If the environment can directly hand work to an agent, follow the user's request and the applicable tool or product boundary; otherwise return the handoff in the current response.

Summarize evidence rather than replaying logs or exhaustive file inventories. Create a saved handoff file only when the user requests one or an established workflow requires one.
