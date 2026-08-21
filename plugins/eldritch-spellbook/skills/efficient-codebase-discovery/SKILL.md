---
name: efficient-codebase-discovery
description: Guide low-overhead codebase discovery before implementation, debugging, review, or planning. Use implicitly only when behavior is unfamiliar, scattered across files, or repeated exact searches would be inefficient. Prefer exact native search for known paths, symbols, strings, errors, or patterns. Use semantic or codebase-search tools only when they are already available, and verify discovered source before relying on it or editing.
---

# Efficient Codebase Discovery

Use the smallest discovery method that can answer the question.

1. Start from the current request, named files, current diff, and already-established context. Do not rediscover known repository structure.
2. Use exact native search and targeted reads when a path, symbol, string, error, filename, or pattern is known.
3. For unfamiliar or scattered behavior, use an available semantic or codebase-search tool when it can reduce broad reading or repeated searches.
4. If no semantic search capability is available, widen native search progressively rather than reading large directory trees or files without a specific reason.
5. Treat search results as leads. Read the relevant source directly before drawing conclusions or editing.
6. Reuse evidence already gathered. Do not repeat equivalent searches unless new information changes the target.

Do not install, configure, authenticate, or require an external search service. Optional tools must improve the current task rather than become a prerequisite for it.

Keep discovery proportional to the work. Stop exploring once enough verified evidence exists to make the next implementation, debugging, review, or planning decision safely.
