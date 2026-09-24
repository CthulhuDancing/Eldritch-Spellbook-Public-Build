---
name: test-design
description: Select, add, or review automated tests for changed behavior, bug fixes, or coverage requests. Reuse existing coverage and justify additions; excludes merely running prescribed checks or diagnosing CI infrastructure.
---

# Test Design

Protect the behavior that matters, with no more coverage than the change
justifies.

## Coverage Flow

Begin with the requested behavior, the current diff, and the tests already
around the affected code. Read the relevant assertions, fixtures, helpers, and
repository test commands. Expand the search only when the contract or existing
coverage is genuinely unclear.

Then make one of three calls:

- **Covered:** keep the existing tests and validate them.
- **Gap:** extend a maintained test or add a focused one.
- **Unclear:** gather the missing evidence before deciding. Do not invent an
   expected behavior just to make a test possible.

For every proposed test, be able to answer three questions: what failure would
it catch, why would the current checks miss that failure, and why does the
failure matter? Base edge cases on the supported contract, an observed defect,
or a concrete risk on the affected path. A merely conceivable case is not
enough. Drop duplicate or speculative tests, and keep the reasoning brief.

When a test is warranted and the change is authorized, follow the repository's
existing conventions and fixtures. Prefer representative inputs and observable
invariants. Use parameterization where it makes the cases clearer, not as an
abstraction exercise. Keep concrete regression inputs that expose a known
defect.

Assert behavior at the smallest useful boundary and derive the expected result
from the contract, independently of the implementation. A good test should
survive a behavior-preserving refactor.

Run the closest maintained checks. For a regression, reproduce the failure
before the fix when practical, then show the check passing afterward. If that
is not possible, say what the validation did and did not establish.

If a check fails, use the result to decide what happens next. Fix a scoped
implementation defect within the user's authorization and rerun the check. If
the test also passes for a known incorrect result, revisit the contract and
revise its inputs or assertions until it distinguishes that failure. If the
contract remains unresolved, report the gap instead of claiming coverage.
Do not treat environment failures, unclear scope, or unresolved behavior as
reasons to add speculative coverage.

Do not repeat an equivalent investigation or edit
unless the state or evidence has changed.

Finish by reporting the coverage decision, its brief rationale, the validation
performed, and any remaining limitation.

## Boundaries

Follow repository-owned requirements and task authorization. Review alone does
not authorize edits. Do not introduce tooling solely to generalize a small
change, pursue test counts without a behavioral reason, or weaken existing
coverage merely to reduce tests or get green. Keep unrelated suite cleanup out
of scope and distinguish unavailable checks from passing checks.
