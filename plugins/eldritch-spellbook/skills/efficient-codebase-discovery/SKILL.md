---
name: efficient-codebase-discovery
description: Locate relevant code, behavior, ownership, or execution paths across local repositories, dependencies, and public upstream projects before implementation, debugging, review, or planning.
---

# Efficient Codebase Discovery

Use the smallest discovery method that can answer the question.

## Discovery Flow

1. Start from the current request, named files, current diff, and
   already-established context. Do not rediscover known repository structure.

2. Classify the target:
   - **Known local target:** use exact native search and targeted reads. Skip
     repository mapping when the relevant path or implementation area is already
     sufficiently known.
   - **Unfamiliar local or runtime-accessible repository:** when the repository is available in the current runtime, run
     `scripts/map_repo.py <repository-root>` first. Use the resulting
     manifests, navigation files, source roots, entry points, code surfaces,
     tests, and documentation paths to guide targeted inspection.
   - **Remote repository without filesystem access:** use the available repository
     or code-search interface to gather equivalent structural evidence without
     first materializing the full repository solely to run the mapping script.
   - **Scattered local behavior:** use the repository map for orientation, then
     use an already-available semantic or codebase-search capability when it can
     materially reduce broad reading or repeated searches.
   - **External project or dependency:** identify the relevant upstream project
     and version or revision when known, then follow
     [references/external-research.md](references/external-research.md).
   - **No useful specialized capability available:** widen native search
     progressively from the strongest known evidence.

3. Treat repository-map output, search results, navigation files, and
   documentation as leads rather than conclusions. Read the relevant
   implementation source directly before drawing conclusions, planning changes,
   or editing.

4. Evaluate whether enough verified evidence exists for the next implementation,
   debugging, review, or planning decision.

5. If more evidence is needed:
   - refine the target using the previous discovery result;
   - narrow, redirect, or widen discovery only when new evidence supports it;
   - follow relevant definitions, calls, configuration, or ownership paths only
     as needed;
   - reuse confirmed findings instead of restarting discovery.

6. Do not repeat an equivalent repository scan, search, directory inspection,
   semantic query, source read, or research path unless the target, repository
   state, version, or available evidence materially changed.

7. Stop when the relevant behavior and ownership boundary are sufficiently
   verified for the next decision, or when further discovery would not produce
   materially new evidence.

## Supporting Resources

Use bundled resources only when they improve the current discovery path.

- Use `scripts/map_repo.py` as the default first-pass orientation tool when an
  unfamiliar repository is available in the current runtime.
- Use `references/external-research.md` when the relevant implementation lives
  in a dependency or public upstream project.

Treat repository-map output as structural evidence, not verified application
behavior.

### `scripts/map_repo.py`

Run:
```bash
python scripts/map_repo.py <repository-root>
```
Available options:
- --json — emit structured JSON instead of text.
- --max-depth N — limit the scan by directory depth.
- --limit N — limit entries shown per summary section.
- Omit <repository-root> to scan the current directory.

## Boundaries

Do not install, configure, authenticate, or require an external search or
research service solely for this workflow.

Do not read large directory trees or files without a specific discovery reason.
Keep discovery proportional to the work.

When external services are used, keep queries limited to public identifiers and
sanitized behavior. Do not expose credentials, private configuration, internal
source, or raw internal logs.

Distinguish verified source behavior from structural evidence and inference.

Discovery does not authorize implementation, repository writes, or unrelated
investigation.