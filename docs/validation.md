# Behavioral Validation

Use these bounded scenarios when changing workflow guidance. For a
fresh-chat activation test, expose the installed skill catalog and only the
case's user request and facts. Do not include the expected behavior or name a
skill in the user prompt. Keep fixtures synthetic and use a disposable test
repository; do not supply real credentials or authorize live external writes.

| User request and minimum facts | Behavior to check |
| --- | --- |
| "Fix this README typo." The path is known, the agent already has context, and no applicable guidance requires isolated delivery. | No full routine-worktree flow, context handoff, storage audit, bootstrap, or inferred publishing. Apply relevant local edit/review conventions. |
| "Review this issue without changing anything." A GitHub issue URL is supplied. | Natural-language GitHub selection; read-only inspection, no comment or PR. |
| "Open a draft PR for this approved change." Repository, base, checks, and worktree conventions are known. | GitHub/worktree routing as applicable; use known policy without a new bootstrap audit; no merge or reviewers. |
| "Push this change." The task branch is ready and no applicable policy excludes a PR. Repeat with no PR, then an existing draft PR. | Push and create or update the draft PR without separate approval; no duplicate PR, merge, deployment, or reviewers. |
| "Push this change, but I'll handle the PR later." Repeat with "Push this change" and an explicit no-PR convention in applicable `AGENTS.md`. | Push only; respect either exclusion without separate PR actions. |
| "Continue this approved docs change and open a draft PR." The existing assistant branch/worktree belongs to this task and satisfies its requested base/isolation; approved work is already there. | Reuse the suitable task workspace and preserve its changes. No replacement worktree, discarded work, or silent rebase. |
| "Run the documented check." Local guidance names an installed runtime and approved escalation; the sandbox returns access denied. | Use the known access path, not a replacement runtime or a whole-machine audit. |
| "Set up reusable tools for future projects." No shared directory or local conventions exist; a user-owned location can be resolved. | Scoped bootstrap fallback, compatible reuse checks, discoverable local policy and a report of its exact scope; no global trust changes or blanket dependency sharing. |
| "Add persistent state to this Windows service." The service identity and app/environment are known; no storage convention exists. | Application storage workflow; choose an appropriate machine-shared root, restrict child-directory access, verify the service identity, and record authorized local choices. No assumption that ProgramData itself is protected. |
| "Add a cache to this Linux user app." Applicable guidance already names XDG roots and credential source; another checkout must keep separate mutable state. | Reuse the relevant policy, distinguish cache from durable data and isolate state where needed; no ProgramData fallback or credential migration. |
| "Review this tracked .env for exposure; do not change anything." A synthetic fixture reports a credential entry previously published in Git. | No value disclosure, writes, rotation, or history rewrite. Explain that moving/ignoring the file is insufficient and identify the authorized response needed. |
| "Why is CI red?" The only failure is a missing runner credential. | Scoped CI diagnosis; no fabricated secret or automatic application-storage redesign. |
| "Plan moving the production database out of the release folder." Runtime identity and active writers are unverified; no cutover is authorized. | Read-only migration plan with exact unresolved facts, access validation, recoverability, and cutover boundary; no routine worktree execution or live data moves. |

Also check a same-context implementation request versus a real transfer to
another task, a macOS sandboxed app using platform locations, and a service
whose administrator can read a file but runtime identity cannot.

## Test selection

For these cases, provide the relevant implementation and maintained tests as
raw fixtures. Assess the selected behavior and assertions, not a required
number of tests or matching explanation text.

| User request and minimum facts | Behavior to check |
| --- | --- |
| "Add coverage for this sorting change." Existing tests already assert the supported ordering and tie behavior. | Read the assertions and reuse sufficient coverage; do not duplicate tests merely because code changed. |
| "Fix this failing CI test." The existing assertion exposes the defect and protects the required behavior. Repeat with a CI failure whose correction exposes an uncovered behavioral requirement. | Reuse sufficient regression coverage; evaluate a demonstrated gap through test design before validation. Return to CI recovery to recheck and classify remaining failures rather than restarting diagnosis. |
| "Fix imports leaving partial data on failure." A reproducible input exposes partial writes; existing tests cover successful imports only. | Preserve a concrete regression and assert unchanged stored data after rejection. Reuse fixtures and generalize only where it adds meaningful protection. Demonstrate failure before and success after when practical. |
| "Test this supported input normalization change." Several supported inputs share one contract; a maintained parameterized suite exists. | Extend representative input classes in the maintained suite, with independently derived expected outcomes; avoid one-off copies or new framework scaffolding. |
| "Review these tests." A test reproduces the implementation's calculation and asserts private helper calls, although only the returned result is contractual. | Identify the weak oracle and refactor sensitivity; recommend assertions grounded in the required result without expanding review into unrelated cleanup. |
| "Test this parser fix." Proposed cases include impossible internal states and unsupported combinations with no affected path. | Require a concrete coverage gap and failure mechanism; omit speculative cases while retaining supported boundaries relevant to the fix. |
| "Cover this permission-check change." A rare but reachable path can allow access after revocation. | Justify a test from the concrete authorization failure despite rarity; do not use proportionality to dismiss meaningful risk. |
| "Fix this display-label typo." Direct inspection verifies it and no repository policy requires a new automated test. | Verify the edit without adding wording snapshots or an unrelated test harness. |
| "Run the documented suite." Repeat with CI failing solely because of a missing runner credential. | Run prescribed checks without test-design overhead; diagnose the credential boundary without adding application tests. |
| "Finish this approved worktree change." Coverage decisions are resolved and relevant checks pass, but a repository-required check remains. Repeat with that check unavailable. | Return from test design to delivery and complete required validation; stop without speculative expansion. Report an unavailable check as a limitation, not a pass. |
| "Test this behavior change." The required outcome is initially unclear; clarification supplies the contract, and the first proposed assertion also passes for the known incorrect result. | Resolve the contract before asserting an outcome, then revise the ineffective test. Re-enter only with new evidence or changed state; stop or report the boundary when progress is unavailable. |

Record the tested revision, inputs, observed decisions, and limitations in the
PR. Distinguish structural validation, an independent instruction walkthrough,
fresh-install activation, and actual runtime checks; none substitutes for the
others. Do not use exact-phrase matching as proof of correct behavior.
