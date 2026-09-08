---
name: agent-context-bridge
description: Prepare compact context handoffs when work moves between chats, tasks, agents, or execution environments, or when completed agent work must be translated back to the originating conversation. Use a project handoff for broad continuation and a targeted handoff for one bounded task. Do not use merely because the user asks the current agent to implement something in its existing context. Preparing a handoff does not authorize invoking an agent or starting implementation.
---

# Agent Context Bridge

Move only the context that improves the receiving agent's work. Prefer confirmed conversation state and named artifacts; inspect repository state only when needed to make the handoff accurate. Use the fields below only when relevant; omit empty sections and do not turn ordinary implementation or completion replies into handoff templates.

## Choose a Forward Lane

### Project Handoff

Use when the receiving agent needs durable context to continue a project or substantial workstream across multiple tasks.

Produce compact Markdown with:

- **Project goal:** the larger outcome being pursued.
- **Current state:** confirmed implementation state and completed work.
- **Decisions:** durable choices the coding agent must preserve.
- **Constraints:** compatibility, safety, scope, and explicit exclusions.
- **Repository orientation:** only the important files, components, branches, or documentation already known to matter.
- **Open work:** prioritized remaining work or the immediate next objective.
- **Validation:** project-owned checks that matter when changes are made.
- **Completion report:** what the receiving agent should return to the originating conversation.

Keep historical narrative out unless it explains a current constraint or decision. Do not make the receiving agent rediscover information already established in chat.

### Targeted Task Handoff

Use for one specific implementation, fix, investigation, refactor, or review task that another agent or task can execute without carrying the whole project conversation.

Produce a focused prompt with:

- **Task:** one concrete outcome.
- **Relevant context:** only facts needed to perform this task correctly.
- **Scope:** named files or components when known, plus adjacent work that must remain untouched.
- **Constraints:** compatibility, safety, preserved behavior, and user decisions.
- **Acceptance checks:** observable conditions that define success.
- **Validation:** known project-owned commands or checks when relevant.
- **Return:** the concise completion information needed back in normal chat.

Do not include broad project history, speculative file lists, or decisions unrelated to the task. Prefer a short executable brief over a comprehensive summary.

## Task Agent to Originating Conversation

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

Carry credential source names and access requirements, never secret values or
unnecessary private data. Sanitize excerpts before including them.
