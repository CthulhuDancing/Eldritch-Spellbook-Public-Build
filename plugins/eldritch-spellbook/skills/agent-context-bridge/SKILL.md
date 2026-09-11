---
name: agent-context-bridge
description: Prepare context handoffs when work moves between conversations, tasks, agents, or execution environments, including results returned to the originating conversation. Do not use for implementation continuing in the current context. Preparing a handoff does not authorize agent invocation or implementation.
---

# Agent Context Bridge

Transfer only context the receiver needs. Prefer confirmed conversation state
and named artifacts; inspect repository state only to resolve material
uncertainty. Omit empty fields, irrelevant history, and speculative file lists.

## Forward Handoff

Choose the scope before writing:

- **Project handoff:** continuation of a project or substantial workstream.
  Include confirmed implementation state, durable decisions, and prioritized
  remaining work.
- **Targeted task handoff:** one implementation, fix, investigation, refactor,
  or review. Include only facts needed for that bounded outcome.

Use these common fields as needed, not as a mandatory template:

- **Outcome:** project goal or concrete task and acceptance conditions.
- **Context:** relevant state, decisions, and known files/components.
- **Scope and constraints:** ownership, preserved behavior, exclusions, and
  material unresolved choices.
- **Validation:** known project-owned checks or other evidence of success.
- **Return:** completion information needed by the originating conversation.

Make the brief executable without requiring rediscovery of established facts.
Do not invent decisions; identify unknowns, and ask only about choices that
block or materially change the receiving task.

## Return Handoff

When results actually move back to the originating conversation, summarize
what changed, verification results, remaining risks, relevant file/task/PR
references, and any next decision. Do not impose this format on ordinary
same-context completion replies.

## Boundaries

A handoff does not authorize repository writes, agent invocation, merges, or
releases. Use a supported transfer mechanism only when the user requests it;
otherwise return the brief here. Save a handoff file only when requested or
required by the established workflow.

Summarize evidence rather than replaying logs. Carry credential source names
and access requirements, never secret values or unnecessary private data;
sanitize excerpts before including them.
