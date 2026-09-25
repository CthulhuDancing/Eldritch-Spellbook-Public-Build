# Repository Normalization Architecture

## Inputs Reviewed

This branch reviewed the complete supplied `Intent.md`, the currently installed `efficient-codebase-discovery` skill, and the current `scripts/map_repo.py` implementation. It also checked authoritative technical documentation for Python archive APIs, Python protocol typing, and Git tracked-file inventory semantics.

The supplied intent defines the target clearly: repository acquisition and normalization must remain deterministic tooling concerns, repository contents should stay outside model context except for later targeted inspection, archives should be inspectable without ordinary extraction where practical, and the local-directory CLI should remain simple.

The current mapper confirms that the problem is narrower than a general repository filesystem problem. Most of the mapper operates on relative file paths. Its direct dependency on a materialized directory is concentrated in two places:

1. obtaining the repository inventory; and
2. opening a small number of structural files, currently `package.json`, to obtain manifest hints.

Authoritative technical facts consulted:

- Git `ls-files` defaults to the cached/index view, which is the tracked-file set used by the current mapper.
- Python `zipfile` exposes member metadata through `infolist()` and supports reading an individual member through `ZipFile.open()` without extracting it.
- Python `tarfile` exposes member metadata and individual member file objects, and also supports sequential stream modes.
- Python `typing.Protocol` supports structural interfaces without requiring adapter classes to inherit from one concrete base class.

## Executive Finding

**Proposed:** Use a small, source-neutral `RepositoryView` protocol backed by source adapters. The protocol should expose:

- a normalized inventory of repository-relative logical paths;
- minimal path metadata needed for safety and optional optimizations;
- provenance/inventory semantics such as local Git index, filesystem walk, remote Git tree, or archive;
- bounded, read-only access to an explicitly requested repository file.

The structural mapper should consume this view rather than a filesystem root. The mapper should materialize the normalized inventory in memory for classification because the current algorithms make several passes over the path set, while file contents remain lazy and are read only for recognized structural files.

A full virtual filesystem is unnecessary. It provides substantially more behavior than the mapper uses and would force remote and archive sources to imitate filesystem operations that are irrelevant to structural mapping.

A serialized repository manifest is useful as an **optional interchange or cache format**, but should not be the primary internal architecture. Making serialization the primary boundary either loses lazy structural-file reads or requires embedding selected contents and classification knowledge into the normalization format.

A second helper script may be useful as a thin producer/diagnostic for a serialized normalized inventory, but it should not own the architecture. The reusable module/protocol should be primary, and `map_repo.py` should remain the ordinary user-facing entry point.

The recommended flow is:

```text
source reference
    |
    v
source resolver / adapter acquisition
    |
    v
RepositoryView
(normalized relative paths + selective read access)
    |
    v
structural classification
    |
    v
existing map data model
    |
    v
text / compact / JSON rendering
```

For remote repositories, the core mapper should not know whether the adapter obtains its tree through a Git implementation, an HTTP API, a provider connector, or another transport. That question belongs beneath the adapter boundary. A remote adapter can depend on a smaller `RepositoryTreeBackend` or equivalent transport interface where needed.

## Current Requirements

### Information the mapper actually needs

**Verified:** The current mapper needs the following information from a repository source:

- repository-relative file paths;
- path component relationships, derivable from those relative paths;
- basenames and suffixes/extensions, derivable from those paths;
- an indication of inventory provenance (`git` versus filesystem today);
- Git tracked-file membership when local Git inventory is available;
- direct readable access to recognized structural files, currently only `package.json` content for manifest hints;
- a displayable root/source identity for the report.

**Verified:** Directory objects are not required. Source roots, test roots, documentation roots, top-level areas, depth, and parent relationships are all inferred from file paths.

**Verified:** General source-code contents are not required to build the structural map. Source contents are not opened merely to count code files, detect directory names, detect conventional entry points, or calculate extension distributions.

**Verified:** The current `package.json` handling reads only these structural fields when present:

- `main`;
- `exports`;
- `bin`;
- `scripts.start`;
- `workspaces`.

### Current local Git semantics

**Verified:** For a directory within a Git repository, the mapper runs `git rev-parse --show-toplevel`, then `git ls-files -z`, and uses the returned tracked paths as its inventory.

**Verified:** `git ls-files` without an alternate selection mode defaults to the cached/index set, so the current inventory represents tracked index paths rather than untracked working-tree files.

**Verified:** After obtaining that Git inventory, the current mapper opens `package.json` through the working-tree filesystem path. Therefore inventory membership comes from the Git index while structural file content comes from the current working tree.

**Inferred:** That mixed behavior should be treated as part of backward compatibility unless there is an explicit decision to change it. For example, an edited but unstaged `package.json` can affect manifest hints while the file inventory remains based on tracked index membership.

### Current non-Git semantics

**Verified:** If Git inventory is unavailable, the mapper walks the filesystem, pruning known generated/vendor directories and optionally pruning by depth.

**Verified:** Git mode applies the depth filter after inventory collection. Filesystem mode can prune traversal at the requested depth.

**Inferred:** A new source-neutral mapper should preserve the semantic result of `--max-depth`, while allowing an adapter to apply the same bound earlier as an optimization where possible.

### Path behavior that is structural, not filesystem-dependent

**Verified:** Once the current file list has been produced, the classifier mostly uses lexical path operations: `name`, `suffix`, `parts`, `parent`, relative path joining, sorting, and POSIX-style rendering.

**Proposed:** Normalize repository paths to `PurePosixPath` or an equivalent logical POSIX path type. Repository paths are logical identifiers, not host filesystem paths. This removes accidental dependence on whether the mapper is running on Windows or POSIX.

## Candidate Architectures

### A. Materialize every source as a temporary directory

```text
source -> download/extract/clone -> temp directory -> existing mapper
```

**Advantages**

- Very small changes to `map_repo.py`.
- Existing filesystem code remains untouched.
- Easy to understand operationally.

**Disadvantages**

- Conflicts with the stated archive-native requirement.
- Introduces filesystem writes solely for structural inspection.
- Reintroduces extraction path and cleanup concerns.
- Remote repositories may require cloning substantially more data than the mapper needs.
- Makes the architecture depend on writable sandbox behavior.
- Treats current implementation convenience as the abstraction boundary.

**Assessment:** Reject as the primary design. It can remain an adapter-specific fallback for a source whose only available transport materializes files, but the mapper should not require it.

### B. Full virtual filesystem

```text
mapper -> VFS operations -> local/archive/remote filesystem implementations
```

A VFS would usually expose concepts such as listing directories, walking trees, stat information, opening paths, existence checks, and sometimes mutation.

**Advantages**

- Familiar abstraction.
- Can model many future sources.
- Could support other tools beyond `map_repo`.

**Disadvantages**

- The mapper does not need directory enumeration APIs once it has a file inventory.
- Remote repository services commonly expose trees/blobs, not general filesystem semantics.
- Archive formats have member tables rather than live directories.
- A broad VFS interface increases testing surface, semantic edge cases, and the temptation to add operations unrelated to structural discovery.
- Filesystem-like random access is awkward for sequential sources such as streamed TAR data.

**Assessment:** Too broad for this problem. A repository inventory/view interface captures the required semantics with less accidental complexity.

### C. Serialized normalized repository manifest

Example conceptual JSONL:

```json
{"schema":1,"path":"server/src/index.js","kind":"file","tracked":true,"size":4812}
{"schema":1,"path":"web/package.json","kind":"file","tracked":true,"size":1320}
```

**Advantages**

- Excellent process boundary.
- Easy to persist, inspect, cache, diff, test, and transfer as an opaque artifact.
- Can be generated by one runtime component and consumed by another without model involvement.
- JSONL can be streamed during production and consumption.

**Disadvantages**

- Paths alone are insufficient for current `package.json` hints.
- Embedding all file contents would defeat the compactness goal.
- Embedding only selected manifest contents forces normalization to know classification policy or creates a second content side channel.
- A permanent serialized schema creates compatibility obligations earlier than necessary.
- Remote and archive adapters would still need a mechanism for selective file retrieval unless all relevant structural contents are embedded.

**Assessment:** Valuable optional interchange format, not the primary in-process abstraction.

### D. Repository inventory protocol with selective content access

```text
source adapter -> RepositoryView -> mapper
```

The view returns normalized entries and can open one logical repository file on request.

**Advantages**

- Directly matches current mapper needs.
- Archives can enumerate members without extraction.
- Remote adapters can enumerate a repository tree and fetch only selected blobs.
- Local Git can keep its current efficient `git ls-files` path.
- Classification code no longer cares how the inventory was acquired.
- New sources add adapters instead of branches throughout the classifier.
- Lazy content access avoids loading general source contents.

**Disadvantages**

- Requires a small refactor of current `root / path` file reads.
- Capability differences such as sequential-only sources must be represented or handled.
- Source resolution and adapter registration require a deliberate design.

**Assessment:** Best primary abstraction.

### E. One-pass path event stream directly into the classifier

```text
adapter -> path events -> incremental classifier -> report
```

**Advantages**

- Minimal inventory memory.
- Fits very large or sequential sources.

**Disadvantages**

- The existing classifier performs multiple logical passes over the inventory.
- Source-root detection, candidate code-surface suppression, sorted output, and later manifest processing are simpler with a retained path set.
- Selected structural file reads may be requested only after the inventory reveals which paths are manifests.
- Rewriting all classification to be stream-oriented would increase complexity for modest practical savings.

**Assessment:** The adapter interface may return an iterator, but the mapper should normally materialize normalized entries before classification. This preserves future streaming acquisition without forcing streaming classification.

### F. Hybrid: repository protocol plus optional serialized snapshot

```text
source -> adapter -> RepositoryView -> mapper
                    |
                    +-> optional normalized JSONL artifact
```

**Advantages**

- Keeps the in-process API simple.
- Supports provider/runtime boundaries that require an artifact handoff.
- Enables debugging and deterministic fixtures without making serialization mandatory.
- Allows future caching without changing classification logic.

**Disadvantages**

- Two representations must be documented if serialization is implemented immediately.

**Assessment:** Preferred overall architecture, with serialization deferred until there is a concrete runtime need.

## Comparison

| Architecture | Local Git efficiency | Archive-native | Remote-friendly | Selective structural reads | Context isolation | Complexity | Extensible source adapters |
|---|---:|---:|---:|---:|---:|---:|---:|
| Temporary directory materialization | High after materialization | Poor | Moderate | Yes | Yes | Low initially, operationally higher | Moderate |
| Full VFS | Moderate | Good | Moderate | Yes | Yes | High | High |
| Serialized manifest only | High | Good | Good | Awkward | Excellent | Moderate | High |
| RepositoryView protocol | High | Excellent | Excellent | Excellent | Excellent | Low-moderate | Excellent |
| One-pass classifier stream | Moderate | Excellent | Excellent | Difficult | Excellent | High | High |
| RepositoryView + optional serialization | High | Excellent | Excellent | Excellent | Excellent | Moderate only when serialization is needed | Excellent |

### In-memory versus serialized representation

**In-memory normalized inventory**

Recommended as the normal mapper working set.

Benefits:

- The current classifier naturally makes repeated passes over paths.
- Path metadata is much smaller than source contents.
- Sorting and cross-path comparisons stay simple.
- No schema/versioning overhead is imposed on ordinary local use.
- The adapter can still produce entries lazily; only the mapper's normalized snapshot is materialized.

Costs:

- Very large repositories still consume memory proportional to path count and path length.
- A hard or configurable entry-count bound is advisable for hostile or accidentally enormous sources.

**Serialized representation**

Recommended only when a durable or cross-process boundary is actually required.

Benefits:

- Reproducible test fixtures.
- Provider/runtime handoff without model ingestion if the runtime can pass opaque files/artifacts.
- Caching and postmortem inspection.
- Easier comparison of adapter output.

Costs:

- Requires schema versioning.
- Does not by itself solve selective file access.
- Risks becoming a second public API.
- If selected contents are embedded, decisions are needed about size, encoding, sensitivity, and which files qualify.

**Proposed:** Keep serialization inventory-only by default. If a future handoff requires selected structural contents too, add an explicitly bounded `structural_blobs` sidecar or content-addressed records rather than broad repository contents.

## Recommended Internal Boundary

The boundary should be split into four layers.

### 1. Source acquisition

Responsibility:

- interpret a source reference;
- select an adapter;
- establish access to the source;
- resolve a remote mutable reference to a stable repository revision where the backend supports that concept;
- obtain any runtime/backend handle without placing repository data into model context.

Examples:

- local path -> local Git or filesystem adapter;
- `.zip` path -> ZIP adapter;
- `.tar.*` path -> TAR adapter;
- remote repository reference -> remote Git/tree adapter using an injected backend.

This layer may be runtime-specific for remote access. It must not leak that specificity into classification.

### 2. Normalization

Responsibility:

- enumerate logical repository files;
- convert names into one canonical relative path form;
- validate path safety and ambiguity;
- provide inventory provenance/tracked semantics;
- provide bounded read-only access to a named logical file;
- optionally expose source capabilities and stable revision identity.

It should **not** decide whether `src/` is a source root, whether `package.json` is a manifest, or whether `main.js` is an entry point. Those are structural classification policies.

### 3. Structural classification

Responsibility:

- apply `max_depth` semantics;
- recognize manifests, navigation files, conventional roots, and entry-point candidates;
- compute counts and distributions;
- request content only for structural files the classifier explicitly understands;
- parse supported manifest hints;
- produce the existing map dictionary/data model.

This layer should receive only normalized logical paths plus the selective read interface.

### 4. Report rendering

Responsibility:

- render the map as text, compact, or JSON;
- remain independent of the source adapter.

The current renderer functions already approximate this boundary and should remain largely unchanged.

## Proposed Interface

The exact names are illustrative; the important part is the semantic boundary.

```python
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import BinaryIO, Iterable, Literal, Protocol


@dataclass(frozen=True)
class RepositoryEntry:
    path: PurePosixPath
    kind: Literal["file", "symlink"] = "file"
    size: int | None = None
    tracked: bool | None = None


@dataclass(frozen=True)
class RepositoryDescriptor:
    display_name: str
    inventory_semantics: str
    revision: str | None = None
    random_read: bool = True


class RepositoryView(Protocol):
    @property
    def descriptor(self) -> RepositoryDescriptor: ...

    def iter_entries(
        self,
        *,
        max_depth_hint: int | None = None,
    ) -> Iterable[RepositoryEntry]: ...

    def open_binary(
        self,
        path: PurePosixPath,
    ) -> BinaryIO: ...
```

### Why `open_binary` rather than `read_text`

**Proposed:** The adapter should expose bytes, while the classification layer owns decoding and size limits for supported structural formats.

Reasons:

- adapters do not need to understand JSON, TOML, or future manifest encodings;
- one policy can enforce maximum structural-file bytes;
- decode errors can be handled consistently;
- archive APIs and remote blob APIs naturally return bytes/file objects.

A classifier helper can then provide bounded reads:

```python
def read_structural_text(view, path, *, max_bytes):
    with view.open_binary(path) as stream:
        data = read_at_most(stream, max_bytes)
    return data.decode("utf-8")
```

Errors should become explicit mapper warnings or absent metadata rather than triggering a fallback in which the model starts retrieving repository contents.

### Normalized path contract

**Proposed:** Every adapter must emit canonical repository-relative logical paths with these invariants:

- POSIX separator semantics;
- no absolute paths;
- no drive-qualified paths;
- no `.` or `..` traversal components after normalization;
- no NUL characters;
- no empty logical path;
- no duplicate file path after normalization;
- a documented policy for symlinks and non-regular archive members.

The mapper should derive directories from these paths rather than require directory entries.

### Inventory semantics

A repository descriptor should distinguish at least:

- `git-index` - current local Git behavior;
- `filesystem` - local non-Git fallback;
- `git-tree` - an immutable or resolved remote Git tree;
- `archive` - file membership supplied by an archive;
- `normalized` - a pre-generated inventory if later supported.

Per-entry `tracked=True` is useful where the source represents Git-tracked entries. For sources where "tracked" has no meaning, use `None` rather than `False`.

### Optional lower-level remote backend

Remote acquisition may need its own backend boundary without exposing provider behavior to `RepositoryView`:

```python
class RepositoryTreeBackend(Protocol):
    def resolve_revision(self, source_ref: str) -> str: ...
    def iter_tree(self, revision: str) -> Iterable[RepositoryEntry]: ...
    def open_blob(
        self,
        revision: str,
        path: PurePosixPath,
    ) -> BinaryIO: ...
```

A `RemoteGitRepositoryView` can delegate to this backend. The backend may later be implemented using a Git-native library, an external service API, or a runtime connector. Structural mapping does not change.

### Mapper refactor shape

Conceptually:

```python
def build_map(view: RepositoryView, max_depth, limit):
    entries = list(view.iter_entries(max_depth_hint=max_depth))

    files = [
        entry.path
        for entry in entries
        if entry.kind in {"file", "symlink"}
        and within_depth(entry.path, max_depth)
    ]

    manifests = [path for path in files if is_manifest(path)]
    manifest_metadata = manifest_hints(view, manifests)

    # Existing structural functions continue from here.
```

The local-directory compatibility wrapper can remain:

```python
def build_map_from_path(path, max_depth, limit):
    view = resolve_local_repository(path)
    return build_map(view, max_depth, limit)
```

## Extensibility

### Local Git adapter

**Proposed:** Preserve the current efficient path almost unchanged:

- `git rev-parse --show-toplevel` identifies the root;
- `git ls-files -z` provides tracked paths;
- paths are normalized into `PurePosixPath` entries;
- `open_binary()` reads from the current working tree.

No serialized inventory, recursive stat calls, or content reads are required.

This retains the current performance characteristic: Git already maintains the tracked inventory, and the mapper does not walk generated or untracked content.

### Local filesystem adapter

Use the current `os.walk()` fallback logic and ignore list. The adapter may honor `max_depth_hint` to prune traversal, while the classifier still applies the depth check to preserve source-independent semantics.

### ZIP adapter

**Verified technical capability:** Python can enumerate ZIP members through the central directory and open a selected member directly without extracting it.

**Proposed behavior:**

- enumerate member metadata;
- ignore directory-only entries;
- validate and normalize names;
- expose uncompressed size when available;
- open selected members read-only through the archive API;
- never call extraction APIs for normal structural discovery.

This maps almost exactly to `RepositoryView`.

### TAR adapter

**Verified technical capability:** Python can enumerate TAR members and obtain a file object for a member without extracting it. TAR also supports sequential stream modes.

**Proposed behavior for ordinary uploaded archive files:**

- scan member headers;
- emit normalized file entries;
- reopen or seek the archive as necessary to read selected structural members;
- avoid filesystem extraction.

A non-seekable TAR stream is a special capability case. The initial architecture does not need to distort the general mapper around it. Such an adapter can either:

1. support a second sequential pass if its source is reopenable;
2. retain only bounded structural members while scanning; or
3. report that selective reread is unavailable and continue without those manifest hints.

That capability should be explicit, not silently emulated through arbitrary extraction.

### Remote Git/tree adapter

A remote adapter should expose the repository tree as the inventory and retrieve only structural blobs requested by the classifier.

**Proposed:** Resolve a branch/tag/ref to a stable revision before inventory and blob reads where the backend permits it. This prevents the normalized path set and manifest content from coming from different remote states.

No model-visible path list is required. The adapter and backend perform acquisition; the model receives only the final compact report.

### Future source adapters

Adding a source should normally require:

1. implementing `RepositoryView` or a small adapter class that produces it;
2. registering a source resolver for that reference type;
3. implementing path validation and bounded selective read semantics;
4. adding adapter contract tests;
5. adding no classification changes unless the new source introduces genuinely new structural evidence.

Possible future adapters include runtime file objects, artifact stores, object storage, alternate Git hosts, or a pre-generated normalized inventory.

### Adapter registration

**Proposed:** Begin with a simple ordered registry of built-in resolvers rather than a dynamic Python plugin system.

For example:

```python
RESOLVERS = [
    LocalDirectoryResolver(),
    ZipArchiveResolver(),
    TarArchiveResolver(),
    RemoteRepositoryResolver(...),
]
```

A dynamic entry-point/plugin mechanism is justified only if third parties actually need to install independent adapters. Premature plugin machinery would add packaging and trust complexity without improving the core seam.

### Second helper script

A second script is useful only for explicit separation needs, for example:

```text
normalize_repo.py <source> --format jsonl
```

Potential uses:

- inspect adapter output;
- generate deterministic test fixtures;
- produce an opaque intermediary artifact for runtimes that cannot keep a live adapter object across a tool boundary;
- cache a large remote tree independently of classification.

**Proposed:** Do not make `map_repo.py` shell out to this script during ordinary local or archive use. Both scripts, if present, should import the same normalization module. This avoids subprocess and serialization overhead becoming mandatory architecture.

## Context-Efficiency Analysis

The context-efficiency requirement is satisfied only if normalization happens entirely outside model reasoning.

### Recommended flow

```text
agent/model
  supplies source reference only
        |
        v
deterministic source adapter
  enumerates repository paths
  reads selected structural files
        |
        v
source-independent mapper
  classifies normalized paths
        |
        v
compact report
        |
        v
agent/model
  sees only structural summary
```

### What remains outside model context

- complete repository path listings;
- archive member tables;
- remote API pagination;
- Git object/tree enumeration;
- general source file bodies;
- normalization records;
- temporary serialized inventories, if any.

### What may enter model context

- the compact map report;
- explicit warnings relevant to map reliability;
- later targeted files selected because the structural map identified them as relevant.

### Why the inventory may still be materialized in process memory

Model context size and process memory are different constraints. Keeping tens of thousands of normalized path records in deterministic process memory does not consume model tokens. Rewriting the mapper into a streaming state machine solely to avoid that memory would increase implementation complexity without addressing the stated failure mode.

### Serialized intermediary caution

A normalized JSONL file is context-efficient only if it remains an opaque runtime artifact consumed by deterministic tooling. If the agent must read the JSONL and pass its contents back into the mapper, the architecture has failed the primary requirement.

## Failure Modes

### Unsafe or ambiguous archive paths

Risk:

- absolute names;
- `..` traversal components;
- Windows drive/UNC-like names;
- path separator ambiguity;
- multiple archive members normalizing to the same logical path.

Mitigation:

- validate before adding an entry;
- reject or explicitly quarantine ambiguous members;
- never extract as part of normal structural mapping;
- reject duplicate normalized paths rather than relying on archive-specific overwrite behavior.

### Archive resource exhaustion

Risk:

- huge member counts;
- extreme path lengths/depth;
- very large structural members;
- compressed content expansion when a selected member is opened.

Mitigation:

- configurable maximum entry count;
- maximum logical path length/depth if needed;
- strict maximum bytes for structural-file reads;
- use archive metadata where available before opening a member;
- stop deterministically with an actionable error rather than falling back to model-driven inspection.

### TAR sequential-access mismatch

Risk:

- a one-pass non-seekable TAR stream cannot necessarily reread `package.json` after the full inventory has been consumed.

Mitigation:

- treat random-read capability explicitly;
- prefer reopenable uploaded archive files for the initial adapter;
- allow a bounded cache of structural candidates or a second pass when necessary;
- do not broaden the core interface into a full VFS to solve this one source shape.

### Remote reference changes during mapping

Risk:

- path inventory from one branch state and manifest content from another.

Mitigation:

- resolve mutable refs to a stable revision before tree and blob operations where possible;
- record the resolved revision in the repository descriptor and report metadata.

### Remote authentication/network failures

Risk:

- retries, credential prompts, rate limits, or unavailable connectors can make deterministic discovery unpredictable.

Mitigation:

- acquisition belongs below the mapper;
- adapters return typed/structured failures;
- credentials remain in the transport/runtime, never in normalized repository data;
- the agent should receive a concise acquisition failure, not be instructed to reconstruct the repository manually.

### Source detection ambiguity

Risk:

- a string can look like a local path, URL, archive, or custom runtime identifier.

Mitigation:

- preserve automatic detection for obvious local directories and recognized archive files;
- allow explicit source-type selection for ambiguous cases;
- keep source resolution outside structural classification.

### Archive wrapper directories

Risk:

- many source archives contain a generated top-level directory such as a repository-and-revision folder;
- blindly stripping every single common prefix can misidentify a legitimate repository whose actual root contains only one directory.

Mitigation:

- make logical-root selection a normalization concern;
- use adapter-known prefix rules when the archive source format guarantees them;
- otherwise use an explicit option or conservative documented heuristic;
- do not bury root guessing in structural classification.

### Inventory/content semantic mismatch

Risk:

- local Git currently lists paths from the index but reads structural content from the working tree.

Mitigation:

- preserve this behavior for backward compatibility in the local Git adapter unless intentionally changed;
- document it;
- remote immutable-tree adapters should use one resolved revision for both inventory and content.

### Structural file read/parse errors

Risk:

- invalid UTF-8;
- malformed JSON;
- unexpectedly large manifest;
- adapter cannot provide the selected file.

**Verified current limitation:** `read_json_file()` catches `OSError` and `JSONDecodeError`, but not `UnicodeDecodeError`, so a non-UTF-8 `package.json` can currently escape the intended empty-hints behavior.

Mitigation:

- centralize bounded structural reads;
- catch decoding failures;
- return an explicit warning plus no hints for that manifest;
- keep the structural path in the manifest list even if metadata parsing fails.

### Over-generalized interface

Risk:

- adding `exists`, recursive `listdir`, `stat`, mutation, extraction, globbing, and arbitrary path operations until the repository view becomes a filesystem framework.

Mitigation:

- require a demonstrated mapper use case before adding protocol methods;
- keep the minimum contract to inventory + selective read + descriptor/capabilities.

### Serialized schema lock-in

Risk:

- an intermediary format becomes a de facto external API and slows internal refactoring.

Mitigation:

- do not serialize by default;
- if serialization is needed, version it explicitly and keep the in-process protocol authoritative.

### Model fallback reappears

Risk:

- an adapter failure causes instructions such as "list the repository through the connector and pass the files to the script," recreating the original context-exhaustion problem.

Mitigation:

- treat inability to acquire/normalize as a tool capability failure;
- report it compactly;
- use another deterministic adapter/transport if available;
- never define manual model normalization as the fallback path.

## Unresolved Questions

1. **Remote acquisition ownership.** Which environments allow deterministic code to call a repository backend directly, and which require a runtime-owned connector/transport? This branch intentionally leaves that behind the remote backend boundary for the provider-specific branch.

2. **Archive logical-root policy.** Should generic uploaded archives preserve their literal root, auto-strip a sole wrapper directory, or require/allow an explicit `--root`/`--strip-prefix` option? A conservative explicit policy is safer than universal guessing.

3. **Symlink semantics.** Should symlink paths count structurally exactly like current local Git paths, and should structural manifest reads ever follow or resolve symlinks for archive/remote sources? The protocol should represent enough information to make this explicit.

4. **Resource bounds.** Exact defaults for maximum member count, selected manifest size, path length/depth, and remote pagination need empirical testing against large legitimate repositories.

5. **Serialized intermediary necessity.** No serialization should be implemented until a runtime boundary actually requires it. If needed, determine whether inventory-only JSONL is sufficient or whether bounded structural blob records are required.

6. **Local Git content source.** Backward compatibility suggests preserving working-tree manifest reads. A future opt-in "committed/index snapshot" mode could instead read blobs from the index or a commit, but that is a different semantic mode and should not silently replace current behavior.

7. **Submodules.** Current `git ls-files` behavior does not recursively map submodule contents. New adapters should preserve that default unless recursive submodule discovery becomes an explicit feature.

8. **Non-UTF-8 Git path fidelity.** The current Git subprocess decodes with UTF-8 and replacement characters. A fully lossless byte-path model would be more correct for pathological repositories but would substantially complicate the normalized interface. This is not required to solve the current architecture problem and should remain a separately justified enhancement.

9. **Warnings in compact output.** The new adapter layer needs a way to expose partial-information conditions without making compact output noisy. A short `warnings:` section only when non-empty is likely sufficient.

## Evidence Classification

### Verified

- The supplied intent requires deterministic normalization outside model context, archive-native inspection where practical, platform neutrality, read-only behavior, and backward-compatible local usage.
- The current CLI accepts a filesystem path and rejects non-existent or non-directory input.
- Local Git inventory uses `git rev-parse --show-toplevel` and `git ls-files -z`.
- Git `ls-files` defaults to tracked files from the index.
- Non-Git inventory uses `os.walk()` with ignored generated/vendor directories.
- Almost all structural classification consumes relative paths rather than file contents.
- Current manifest content access is direct filesystem access and currently only parses `package.json` for structural hints.
- Current Git inventory and working-tree manifest content can represent different repository states.
- ZIP member metadata and selected member content can be inspected through Python APIs without ordinary extraction.
- TAR member metadata and selected member content can be inspected through Python APIs without ordinary extraction; sequential stream modes also exist.
- Python protocols support structural interfaces suitable for adapter contracts.
- The current JSON reader does not catch `UnicodeDecodeError`.

### Inferred

- The smallest useful seam is inventory acquisition plus selective structural-file access, because those are the current filesystem-coupled operations.
- Directory objects are unnecessary because all directory relationships used by the mapper can be reconstructed from normalized file paths.
- Materializing path metadata in deterministic process memory is compatible with the context-efficiency goal because model token usage is the target constraint, not zero process memory.
- Remote repository consistency is improved by resolving a mutable ref before listing paths and fetching structural blobs.
- Preserving local Git index inventory plus working-tree structural reads is the least surprising backward-compatible default.
- A one-pass streaming classifier would add more complexity than it saves for the current mapping algorithms.

### Proposed

- Make `RepositoryView` the primary internal abstraction.
- Implement source-specific adapters for local Git, local filesystem, ZIP, TAR, and remote repository trees.
- Normalize logical repository paths to canonical relative POSIX paths, preferably represented as `PurePosixPath`.
- Keep structural classification and report rendering source-independent.
- Expose binary selective reads and centralize bounded decoding/parsing in the classifier.
- Materialize only normalized entry metadata in memory; keep file contents lazy.
- Treat a serialized inventory as optional interchange/cache, not the primary architecture.
- Use a second normalization script only as a thin optional front end over the same module, not as a mandatory subprocess stage.
- Put provider/network specifics behind a remote backend or transport beneath the repository adapter.
- Preserve the existing local CLI form, with source auto-resolution added behind it.
- Add explicit bounds, path validation, duplicate rejection, revision metadata, and concise warnings so hostile or partially readable sources fail deterministically rather than pushing normalization back onto the model.

The preferred architecture is therefore a **small repository inventory/view protocol plus source adapters, with an in-memory normalized path snapshot and lazy bounded structural-file reads**. It changes the mapper at the narrowest meaningful dependency boundary while avoiding both extremes: materializing every source as a filesystem and inventing a general VFS that the mapper does not need.
