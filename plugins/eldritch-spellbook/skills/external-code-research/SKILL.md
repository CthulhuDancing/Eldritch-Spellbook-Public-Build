---
name: external-code-research
description: Research public upstream repositories or dependency internals when an external implementation detail matters. Use for libraries, frameworks, or public repositories; do not use for the current repository, general documentation lookup, or ordinary local code discovery.
---

# External Code Research

Investigate only the external implementation detail needed for the current
question. Keep this work read-only and separate from local codebase discovery.
Keep external queries limited to public identifiers and sanitized behavior;
do not send local credentials, private configuration, or raw internal logs.

1. Identify the upstream project, package version or revision when known, and
   the concrete behavior to understand.
2. Start with the smallest authoritative source available: installed matching
   source, official project documentation, or the public repository.
3. Use an available repository or code-search tool when it reduces exploration;
   do not install, configure, authenticate, or require one.
4. Use multiple independent research angles only when the question genuinely
   spans separate concerns. Otherwise, make one focused inquiry.
5. Read the relevant upstream source before relying on search results. Distinguish
   verified behavior from an inference about how it applies locally.
6. Return the source revision or version, relevant files or entry points, the
   behavior found, and the smallest useful implication for the current task.

Do not modify the upstream project, treat an external pattern as a requirement
for the local repository, or expand the work into a local implementation unless
the user asks.
