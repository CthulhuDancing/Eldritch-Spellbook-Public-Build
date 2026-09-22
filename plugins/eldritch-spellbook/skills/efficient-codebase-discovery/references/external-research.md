# External Research

Use this route when the relevant implementation lives in a dependency, public
upstream repository, framework, library, or other external codebase.

## Source Selection

Prefer the smallest authoritative source that can answer the question:

1. Matching installed source when available and trustworthy.
2. Official project documentation for documented behavior.
3. The authoritative public repository for implementation details.

Identify the relevant package version, release, commit, or revision when it can
materially affect behavior.

## Research Flow

1. Start from the concrete external behavior or implementation detail that
   needs explanation.

2. Use concise navigation sources, repository structure, indexes, manifests,
   documentation, or available code search to narrow the likely implementation
   before reading broad source trees.

3. Read the relevant upstream source directly before treating search results,
   summaries, or documentation as evidence of implementation behavior.

4. If the evidence is incomplete:
   - follow relevant definitions, calls, configuration, or version-specific
     paths;
   - refine the target using the previous source inspection;
   - use another research angle only when the evidence points to a genuinely
     separate concern.

5. Stop when the upstream behavior is sufficiently verified for the current
   decision.

## Reporting

Distinguish:
- verified upstream behavior;
- version or revision assumptions;
- inference about how that behavior may apply locally.

Capture the relevant source version or revision, important files or entry
points, and the smallest useful implication for the current task.

## Boundaries

Do not treat an external implementation pattern as a requirement for the local
repository.

Do not modify the upstream project or expand research into local implementation
unless the current task calls for it.

Keep external queries limited to public identifiers and sanitized behavior.