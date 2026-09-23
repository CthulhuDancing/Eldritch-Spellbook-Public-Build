---
name: test-design
description: Select, add, or review automated tests for changed behavior, bug fixes, or coverage requests. Reuse existing coverage and justify additions; excludes merely running prescribed checks or diagnosing CI infrastructure.
---

# Test Design

Protect meaningful behavior with the smallest justified coverage change.

## Coverage Flow

1. Start from the requested behavior, current diff, and known context. Inspect
   relevant assertions, fixtures, helpers, and repository-owned test commands.
   Widen discovery only when coverage or the expected behavior remains unclear.

2. Classify the coverage decision:
   - **Sufficient coverage:** reuse it and proceed to validation.
   - **Demonstrated gap:** identify the missing behavioral protection and propose
     extending a maintained test or adding one.
   - **Unclear behavior or coverage:** inspect the missing evidence, then
     reassess; do not invent expected behavior to write a test.
   - **Low-impact change with adequate direct verification:** add no automated
     test unless repository guidance requires one.

3. Challenge each proposed test or behavior group: what plausible failure would
   it catch, why would existing checks miss it, and why does that failure matter?
   Ground edge cases in supported behavior, observed defects, or concrete risks
   on affected paths. Possibility alone is insufficient; rarity alone does not
   dismiss a credible high-impact failure.

   Discard duplicate or speculative proposals. Revise weak assertions or return
   to discovery when the contract is unclear. Keep the justification brief.

4. For justified, authorized changes, reuse existing test conventions and
   fixtures. Prefer representative input classes and meaningful invariants;
   use parameterization when useful without building unnecessary abstractions.
   Preserve concrete regression inputs that expose known defects.

   Assert observable behavior at the smallest boundary that exposes the risk.
   Derive expected results independently from the contract. Tests should survive
   behavior-preserving refactors rather than mirror implementation details.

5. Run the closest maintained checks and complete required validation. For a
   regression, demonstrate failure before the fix and success afterward when
   practical. Otherwise explain the verification limit.

6. Evaluate the result:
   - **Gap addressed and required checks pass:** finish.
   - **Scoped implementation defect:** correct it within authorization, then
     recheck.
   - **Test does not distinguish correct from incorrect behavior:** return to
     test design without weakening the contract.
   - **Environment failure or unresolved scope/behavior:** route to appropriate
     diagnosis or report the boundary; do not add speculative tests.

7. Repeat discovery, edits, or checks only when changed state or new actionable
   evidence supports another attempt. Stop when complete or further work cannot
   make evidence-driven progress. Report the coverage decision, brief rationale,
   validation performed, and unresolved limits.

## Boundaries

Follow repository-owned requirements and task authorization. Review alone does
not authorize edits. Do not introduce tooling solely to generalize a small
change, pursue test counts without a behavioral reason, or weaken existing
coverage merely to reduce tests or get green. Keep unrelated suite cleanup out
of scope and distinguish unavailable checks from passing checks.
