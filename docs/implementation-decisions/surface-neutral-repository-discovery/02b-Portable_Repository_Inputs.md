# Portable Repository Inputs

## Inputs Reviewed

This report evaluates the smallest practical source mechanics needed to extend the current local-directory-only repository mapper described in `Intent.md`. The design target is deterministic structural discovery with minimal model-context use, direct archive inspection without filesystem extraction, and a provider-neutral core wherever practical.

The source forms reviewed are:

- existing local directory paths;
- local or runtime-materialized ZIP archives;
- local or runtime-materialized TAR-family archives;
- remote Git repository URLs or identifiers;
- provider-specific repository identifiers;
- future opaque runtime file or artifact references.

**Verified:** The current mapper accepts only an existing directory, uses `git ls-files -z` when Git inventory is available, otherwise falls back to filesystem traversal, and directly opens structural files such as `package.json`. The stated design goal is to keep repository normalization outside model context and to inspect uploaded archives without normal extraction. See `Intent.md`, especially its current-behavior, archive, context-isolation, and platform-neutrality sections.

**Verified:** Python's standard library provides direct read APIs for ZIP and TAR archives. `zipfile.ZipFile.infolist()` exposes members and `ZipFile.open()` opens a selected member as a read-only binary stream. `tarfile` supports transparent reads of common TAR compression formats, exposes `TarInfo` metadata, and `TarFile.extractfile()` returns a file object for a selected regular member. These operations do not require extracting the archive tree to disk.

**Proposed:** Treat archive files as repository snapshots with their own inventory provenance, not as implicit Git repositories. Preserve the current Git-backed inventory when an actual local Git checkout is present.

## Executive Finding

**Verified:** Direct, non-extracting inspection of ZIP and TAR-family archives is practical with portable Python facilities. Both formats provide enough metadata to enumerate relative member paths, identify directories, inspect type/size information, and selectively read a small number of manifest or navigation files.

**Inferred:** This is sufficient for the current mapper's structural needs because its primary inputs are path structure plus selected root-level metadata, not arbitrary source contents.

**Proposed:** The minimum first implementation should support three concrete inputs:

1. an existing local directory;
2. a ZIP archive available as a local path or seekable binary file object;
3. a TAR-family archive available as a local path or seekable binary file object.

The archive readers should never call extraction APIs. They should normalize validated member names into logical repository-relative POSIX-style paths, expose only bounded selected-member reads, and label the inventory source as `archive-members` (or similar) rather than `git-tracked`.

Remote Git URLs should be accepted only as an identifiable source class at this stage, not acquired by the portable core. A URL is portable as a reference string, but network access, authentication, provider APIs, connector use, and artifact handoff are external-acquisition concerns and therefore need adapters. Provider-specific IDs and opaque runtime file references also inherently need adapters unless the runtime first exposes them as a normal path or file-like object.

This directly supports the intent requirement that the model provide a source reference while deterministic tooling performs the structural work, rather than reconstructing repository structure in model context.

## Source Types

### Local directory

**Verified:** This is the existing supported input and should remain the simplest path. When the directory is a Git worktree and Git is available, `git ls-files` can continue to supply the tracked-file inventory. Git documents `git ls-files --cached` as listing files in the index, i.e. tracked files.

**Proposed:** Preserve existing CLI behavior for directory paths without forcing them through an archive abstraction.

### ZIP archive

**Verified:** A ZIP file can be enumerated and selectively read without extraction using the Python `zipfile` module. A seekable file-like object can also be supplied to `ZipFile`, which is useful for future runtime adapters.

**Proposed:** Treat accepted ZIP members as a snapshot inventory. Do not attempt to infer Git tracked/untracked state from `.gitignore` or other files.

### TAR-family archive

**Verified:** Python `tarfile` can read uncompressed TAR and common compressed forms. Python 3.12 supports gzip, bzip2, and xz/lzma TAR reads; Python 3.14 also documents Zstandard TAR support. `r:*` performs transparent compression detection.

**Proposed:** Guarantee `.tar`, `.tar.gz`/`.tgz`, `.tar.bz2`, and `.tar.xz` where the standard modules are available. Treat `.tar.zst` as feature-detected rather than universally guaranteed unless the project sets Python 3.14+ as its minimum runtime.

### Remote Git repository reference

**Verified:** Git itself recognizes multiple repository URL forms, including HTTPS, SSH, `git://`, local paths, and `file://`. This means a remote repository can be represented as a string without choosing a provider API.

**Inferred:** Representation is portable; acquisition is not. A restricted runtime may not expose network access, Git credentials, a Git executable, or a provider connector to deterministic code.

**Proposed:** Parse/classify a remote identifier but route acquisition through an external adapter boundary. Do not make remote URL support a prerequisite for the archive implementation.

### Provider-specific repository identifier

Examples include an owner/repository tuple, provider object ID, connector resource ID, or repository object returned by a native tool.

**Inferred:** These are not platform-neutral because their interpretation and authentication are provider-specific.

**Proposed:** Keep them outside the core source syntax. An adapter can convert them into either a local/seekable archive or another normalized inventory later.

### Opaque runtime file or artifact reference

**Inferred:** An opaque handle is usable by the portable archive layer only after the runtime adapter exposes bytes, a seekable binary stream, or a local path. The handle itself has no portable semantics.

**Proposed:** Prefer an adapter contract that returns either a filesystem path or a seekable binary file object. This matches both `zipfile` and ordinary random-access `tarfile` use and avoids requiring the core to know runtime-specific handle types.

## ZIP Analysis

### Enumeration

**Verified:** `ZipFile.infolist()` returns one `ZipInfo` per archive member in archive order. `ZipFile.namelist()` returns names only. `ZipInfo.is_dir()` identifies directory entries by the trailing slash convention.

For structural mapping, `infolist()` is the better primitive because it preserves per-member metadata such as:

- member name;
- directory status;
- compressed and uncompressed size;
- CRC;
- archive-order identity;
- creator/system attributes.

It also allows duplicate names to remain distinguishable because later reads can use the specific `ZipInfo` object rather than looking up by a string name.

### Selected content reads

**Verified:** `ZipFile.open(member, 'r')` returns a binary, read-only `ZipExtFile`. It accepts a `ZipInfo` object, which is important when duplicate names exist.

**Proposed:** Store the exact accepted `ZipInfo` object behind each normalized logical path and read manifests through that object. Apply a per-member byte limit before parsing. `ZipInfo.file_size` provides a useful declared uncompressed-size precheck; the actual read should still be bounded.

### Path normalization

**Verified:** ZIP member names are archive names, not automatically safe logical repository paths. Python specifically warns that `zipfile.Path` does not sanitize archive filenames and leaves path-traversal validation to the caller.

**Proposed:** Do not use archive member names as filesystem paths and do not join them to a writable directory. Convert only validated names into logical POSIX repository-relative paths. Reject or flag at least:

- absolute names;
- `..` path components;
- empty or NUL-containing names;
- names whose canonical form escapes the logical repository root;
- ambiguous backslash-containing paths if cross-platform repository semantics are required.

A direct archive reader does not need `ZipFile.extract()` or `extractall()` at all.

### Links and special cases

**Verified:** ZIP does not expose a first-class, cross-platform `ZipInfo.is_symlink()` API comparable to TAR's type methods. Unix-origin ZIP tools may encode mode information in external attributes, but that encoding is not a portable guarantee across producers.

**Proposed:** Do not follow or emulate ZIP symlinks. Where a symlink can be detected reliably from Unix mode metadata, classify its path as a link-like member and refuse manifest-content reads through it. Where it cannot be detected, treat the member as opaque archive content rather than attempting filesystem link semantics.

### Duplicates and malformed files

**Verified:** ZIP archives may contain duplicate member names; Python explicitly supports passing `ZipInfo` objects to distinguish them. Invalid ZIPs raise `BadZipFile`. Unsupported compression/decryption or resource exhaustion can also prevent reads. Python documents decompression bombs as a resource-risk class.

**Proposed:** A repository snapshot should have one authoritative entry per logical path. In strict mode, duplicate canonical paths should therefore fail normalization rather than silently selecting one. This is simpler and safer than inventing overwrite semantics for a structure that is supposed to model a repository tree.

## TAR Analysis

### Enumeration

**Verified:** `tarfile.open(..., mode='r:*')` can transparently read supported compressed or uncompressed TAR files. TAR members are represented as `TarInfo` objects. `TarInfo` distinguishes regular files, directories, symbolic links, hard links, FIFOs, character devices, and block devices.

**Proposed:** For the repository inventory, collect validated paths for normal file-like repository entries and directories, but do not materialize special filesystem objects. Directories are useful for structural relationships but should not count as source files.

### Selected content reads

**Verified:** `TarFile.extractfile(member)` returns a binary file object for regular files and links; other member types return `None`.

**Proposed:** Call `extractfile()` only for `TarInfo.isreg()` members selected for manifest/navigation reads. Do not use it to dereference symlinks or hard links. Precheck `TarInfo.size`, then perform a bounded read.

### TAR-family portability

**Verified:** Current Python documentation supports gzip, bzip2, lzma/xz, and, in Python 3.14, Zstandard when the corresponding module is available. Python 3.12 does not provide the documented Zstandard TAR mode.

**Proposed:** Use capability detection rather than filename-only promises. The portable baseline should be TAR, TAR.GZ/TGZ, TAR.BZ2, and TAR.XZ. Add TAR.ZST when the executing Python exposes it.

### Links, devices, and duplicate names

**Verified:** TAR can encode symlinks, hard links, FIFOs, character devices, block devices, and other Unix filesystem semantics. Python's extraction documentation treats these features as security-relevant. It also documents that a TAR may contain multiple occurrences of the same member name and that later occurrences are normally considered the most up-to-date.

**Proposed:** Structural discovery does not need to recreate those semantics. Include a symlink/hard-link path only as a typed logical entry if useful to file counts and topology; never follow it for content discovery. Reject device/FIFO/special members from the logical repository file inventory. Treat duplicate canonical paths as a normalization error by default, despite TAR's extraction-oriented last-occurrence convention.

### Malformed archives

**Verified:** `tarfile` raises `ReadError` when an archive cannot be handled or is invalid and `CompressionError` when a compression method is unsupported or cannot be decoded.

**Proposed:** Normalize these to a small source-reader error surface, such as `unsupported archive`, `malformed archive`, `unsafe member`, and `limit exceeded`, rather than leaking format-specific exceptions to mapper logic.

## Archive Safety Boundary

Avoiding extraction materially simplifies the security boundary, but it does not make arbitrary archive input free of risk.

### Advantages of no extraction

**Verified:** Both Python ZIP and TAR documentation warn about dangerous extraction paths and archive members. TAR documentation specifically calls out absolute paths, `..` components, symlink effects, and special files as extraction hazards.

**Inferred:** If structural discovery never writes members to disk, then path traversal cannot overwrite files outside an extraction directory, archive symlinks cannot redirect later filesystem writes, device entries cannot create devices, and permission/ownership metadata is never applied.

**Proposed:** The archive source layer should expose no extraction operation. Its public capabilities should be limited to:

- enumerate normalized member metadata;
- open a bounded, explicitly selected regular member for reading;
- report archive/source metadata.

### Remaining risks

**Verified:** Python's documentation warns that decompression bombs and other resource exhaustion remain possible. TAR extraction guidance recommends limits on member count, total size, filename length, individual file size, memory, and CPU.

**Inferred:** Those resource risks also apply to read-only structural inspection, especially for compressed TAR streams that must be decompressed to scan headers and for selected highly compressed ZIP members.

**Proposed:** Enforce configurable bounds before or during enumeration/read operations, including:

- maximum archive input size where known;
- maximum member count;
- maximum member-name length;
- maximum selected-member uncompressed size;
- maximum total bytes read for structural content;
- optional compression-ratio or declared-size sanity checks;
- time/CPU limits supplied by the host runtime where possible.

Do not run a full `testzip()` or equivalent validation pass merely to obtain structure; that would decompress content the mapper does not otherwise need.

### Logical path safety

**Inferred:** Even without filesystem writes, traversal-like names can corrupt root detection, produce misleading path relationships, or collide after normalization.

**Proposed:** Validate names before classification and preserve a one-to-one canonical logical path map. Never use `resolve()` against the host filesystem for archive-internal paths; these are logical repository paths, not host paths.

## Repository Root Detection

Archives frequently add a wrapper directory such as `project-main/`, while the mapper expects repository-relative paths such as `package.json`, `src/app.py`, or `README.md`.

**Verified:** Git's `git archive --prefix=<prefix>/` deliberately prepends a directory prefix to archived paths. Hosted archive services may also return prefixed archive snapshots. Therefore a wrapper is normal archive behavior, not necessarily part of the repository tree.

**Inferred:** A single common first path component is a useful wrapper candidate, but it is not proof. A legitimate repository can itself contain all tracked files beneath one directory and have no root-level files.

**Proposed:** Root handling should be conservative and explicit:

1. Canonicalize and validate member names first.
2. Ignore directory-only entries when deciding whether every file-like member shares a common first component.
3. Detect a common first component as a *candidate* wrapper.
4. Auto-strip it only when corroborating evidence exists, for example when stripping exposes recognized repository-root markers such as manifests/navigation files, or when source metadata identifies the wrapper.
5. Otherwise retain the archive root and report the candidate as ambiguous.
6. Allow a future explicit `root_prefix`/`archive_root` override rather than adding increasingly complex heuristics.

This keeps root detection small and avoids turning archive normalization into repository-content reasoning.

## Remote Identifier Analysis

Remote repository references should be separated into representation and acquisition.

### URL representation

**Verified:** Git supports standard transport forms including HTTPS and SSH repository URLs. A URL such as `https://github.com/org/repo` is therefore a plausible generic source reference string.

**Inferred:** A URL alone does not define how a restricted runtime should retrieve repository contents. Network access, authentication, ref selection, Git availability, host APIs, rate limits, and connector permissions all vary by environment.

**Proposed:** Treat remote URLs as opaque remote-source identifiers at the portable boundary. A host adapter should be responsible for turning the URL plus optional ref into one of the portable core forms:

- a local directory;
- a local archive;
- a seekable archive stream;
- or a future normalized repository inventory.

### Provider-specific identifier

**Inferred:** Forms such as `github:org/repo`, connector resource IDs, installation-scoped IDs, or native repository objects cannot be interpreted without the corresponding provider/adapter.

**Proposed:** Do not bake these into the first CLI contract. They can be adapter inputs later.

### Remote archives and Git semantics

**Verified:** Git can create ZIP or TAR snapshots using `git archive`, and `git archive` may apply `export-ignore`; it can also add non-tracked files with `--add-file`. Therefore even a Git-produced archive is not universally identical to `git ls-files` output.

**Inferred:** A provider-downloaded source archive should be treated as a repository *snapshot* rather than asserted to be the exact Git index inventory unless the acquisition adapter has stronger provenance guarantees.

**Proposed:** Preserve provenance in output, for example `inventory_source=git-index`, `filesystem-walk`, or `archive-members`, so the agent can distinguish tracked-file certainty from archive-snapshot semantics.

## Portability Matrix

| Input form | Core can recognize | Core can inspect without extraction | External acquisition required | Git-tracked semantics | Portability judgment |
|---|---:|---:|---:|---|---|
| Existing local directory path | Yes | N/A | No | Yes when Git worktree + Git CLI are available; otherwise filesystem fallback | High |
| Local ZIP path | Yes | Yes | No | No; archive snapshot semantics | High |
| Seekable ZIP file object | Yes, as library API | Yes | Adapter only if runtime owns the handle | No; archive snapshot semantics | High once bytes/stream are exposed |
| Local TAR/TAR.GZ/TGZ/TAR.BZ2/TAR.XZ path | Yes | Yes | No | No; archive snapshot semantics | High |
| TAR.ZST path | Feature-detect | Yes where supported | No | No; archive snapshot semantics | Medium across Python versions; high on 3.14+ |
| Seekable TAR file object | Yes, as library API | Yes | Adapter only if runtime owns the handle | No; archive snapshot semantics | High once bytes/stream are exposed |
| Non-seekable TAR stream | Technically possible | Yes, one pass | Usually adapter | No | Medium; complicates later selected reads |
| Remote Git HTTPS/SSH URL | Yes as a string/source class | Not by core alone | Yes | Depends on acquisition method | Reference is portable; acquisition is not |
| Provider-specific repo identifier | Only via adapter registration | Depends on adapter | Yes | Depends on adapter | Low at core boundary |
| Opaque runtime file/artifact handle | No intrinsic meaning | Only after adapter exposes data | Yes | Depends on payload | Adapter-only |

## Minimum Viable Input Set

The smallest first implementation that solves the immediate runtime problem should be:

### 1. Preserve local directories

**Proposed:** Keep the existing command behavior for ordinary repository directories. Continue using Git inventory where available and the existing fallback where it is not.

### 2. Add direct ZIP input

**Proposed:** If the supplied path is a ZIP archive, enumerate `ZipInfo` records, validate/canonicalize member names, detect an optional wrapper root, and expose selected regular members through bounded `ZipFile.open()` reads. Never extract.

### 3. Add direct TAR-family input

**Proposed:** If the supplied path is a supported TAR-family archive, enumerate `TarInfo` records, validate/canonicalize names, ignore/reject unsupported special members, detect an optional wrapper root, and expose selected regular members through bounded `extractfile()` reads. Never extract.

### 4. Make the archive reader internally file-object capable

**Proposed:** Even if the CLI initially accepts only filesystem paths, write the archive-opening layer so a seekable binary file object can be supplied by a future adapter. This is a small portability gain because both standard-library archive modules already support file-like inputs.

### 5. Do not claim Git equivalence for archive inventories

**Proposed:** Use a distinct inventory label such as `archive-members`. The logical inventory should consist of accepted file-like paths in the snapshot after wrapper normalization. Do not implement `.gitignore` processing as a substitute for Git tracking; ignore rules do not reconstruct the Git index.

This set directly handles local checkouts and uploaded archives when the runtime exposes the upload as a path or file-like object. It also creates the smallest useful handoff target for later provider-specific acquisition work.

## Deferred Inputs

The following should be deliberately deferred from the first source-mechanics implementation:

- direct HTTP/Git network acquisition;
- authentication and credentials;
- OpenAI-, Anthropic-, GitHub-, GitLab-, Bitbucket-, or other provider-specific connector behavior;
- provider-native opaque artifact IDs beyond an adapter interface;
- Git object database or index parsing in pure Python;
- bare repositories and Git bundles as first-class inputs;
- automatic clone/fetch behavior;
- submodule expansion;
- Git LFS object expansion;
- encrypted/password-protected archives;
- multi-volume archives;
- RAR, 7z, and other non-stdlib formats;
- nested-archive recursion;
- full ZIP symlink fidelity across arbitrary producers;
- TAR special-file reconstruction;
- non-seekable stream support as a first-class general input;
- aggressive repository-root heuristics that inspect substantial source content;
- filesystem extraction as a normalization strategy.

**Proposed:** TAR.ZST can be enabled opportunistically through runtime feature detection, but should not be part of a broad compatibility promise unless the minimum Python version guarantees it.

## Failure Modes

### Unsafe or ambiguous member paths

Absolute paths, `..` components, embedded control characters, ambiguous separators, or canonical-path collisions should fail or be excluded according to a documented strict policy. They must never be resolved by writing to the host filesystem.

### Duplicate logical paths

ZIP and TAR can both represent duplicate names. A repository tree cannot meaningfully expose two simultaneous files at the same path. Strict normalization should reject duplicates rather than hide archive ambiguity.

### Wrapper false positives

A single common first directory is not sufficient proof of an archive wrapper. Conservative auto-detection may leave some wrappers unstripped; aggressive auto-detection may incorrectly remove a real repository directory. This is a policy tradeoff, not an archive-library limitation.

### Symlink ambiguity

TAR has explicit link types; ZIP symlink metadata is producer-dependent. Structural inventory can preserve a link path without following it, but exact cross-format link equivalence should not be promised.

### Special TAR members

Device nodes, FIFOs, and similar entries have no useful role in repository structural mapping and should be rejected or ignored rather than reproduced.

### Resource exhaustion

Malformed or hostile archives can contain extreme member counts, enormous declared sizes, very large path names, sparse members, or highly compressed data. No-extraction reduces write risk but not CPU/memory/decompression risk. Limits are required.

### Unsupported compression

TAR compression availability varies with Python/runtime modules. ZIP members can also use compression methods unavailable to a particular runtime. Report unsupported compression distinctly from general corruption.

### Corrupt archives

ZIP `BadZipFile`, TAR `ReadError`, checksum/CRC failures, truncated data, unsupported encryption, and decompressor failures should become deterministic source-reader errors.

### Non-seekable inputs

ZIP's central-directory design normally requires seeking. TAR can be streamed, but one-pass streaming complicates the mapper's pattern of first building structure and later reading selected manifests. Requiring a path or seekable binary stream is the simpler first contract.

### Archive inventory differs from Git index

Arbitrary uploaded archives can include untracked files or omit tracked files. Even `git archive` may honor `export-ignore` or add explicit non-tracked files. The output must not mislabel archive membership as `git ls-files` equivalence.

### Remote reference without acquisition adapter

A remote URL can be syntactically valid but unusable in the current runtime. This should fail as `remote source requires acquisition adapter`, not fall back to model-driven manual repository reconstruction.

## Unresolved Questions

1. What minimum Python version will the skill support? This determines whether TAR.ZST can be guaranteed and which `tarfile` hardening features are universally present.
2. What default bounds should apply to archive byte size, member count, member-name length, per-member read size, and total structural bytes read?
3. Should duplicate logical paths be a hard error in all modes, or should a compatibility mode expose deterministic last-entry semantics?
4. What exact root-marker set should corroborate automatic wrapper stripping?
5. Should the CLI expose an explicit archive-root override in the first archive release, or only after a real ambiguous case appears?
6. Should symlink and hard-link paths count toward ordinary file counts, or be reported separately as typed entries?
7. What adapter result type will the provider-runtime branch choose: local path, seekable binary stream, downloaded archive artifact, or a higher-level inventory interface?
8. If a runtime exposes an opaque file handle but only non-seekable reads, should the adapter buffer it to a bounded temporary file/memory object, or should the core add streaming TAR support?
9. Should remote references include a ref/commit as a separate field rather than embedding host-specific ref syntax in a URL?
10. Should archive provenance include a known commit/ref when the acquisition adapter can supply one, while still retaining `archive-members` inventory semantics?

## Evidence Classification

### Verified

The following findings are directly supported by the provided intent or first-party documentation:

- The current mapper is local-directory-centric, uses `git ls-files` where possible, and directly opens structural files.
- The design requires archive-native inspection without normal extraction and seeks to keep repository normalization out of model context.
- Python `zipfile` can enumerate `ZipInfo` members and selectively open a member as a binary stream.
- Python warns that `zipfile.Path` does not sanitize member names.
- Python `tarfile` can enumerate typed `TarInfo` members and selectively open regular member data.
- TAR supports filesystem types that are unsafe or irrelevant to repository structural mapping, including links and device-like members.
- Python archive documentation warns that extraction filters do not eliminate all resource/denial-of-service risks.
- Current Python `tarfile` supports transparent common compression formats; Python 3.14 adds documented Zstandard TAR support.
- Git `ls-files` describes tracked/index inventory semantics.
- Git accepts multiple remote URL transports.
- `git archive` can prepend a prefix and can produce TAR/ZIP snapshots; attributes such as `export-ignore` and explicit `--add-file` can make an archive differ from a plain tracked-file list.

Primary sources:

- Provided `Intent.md` / `01-Intent.md`.
- Python `zipfile`: https://docs.python.org/3/library/zipfile.html
- Python `tarfile`: https://docs.python.org/3/library/tarfile.html
- Git `git-ls-files`: https://git-scm.com/docs/git-ls-files
- Git `git-clone` URL forms: https://git-scm.com/docs/git-clone
- Git `git-archive`: https://git-scm.com/docs/git-archive
- GitHub repository archive API example, useful only as evidence that remote hosts can expose archive snapshots and not as a provider-neutral acquisition prescription: https://docs.github.com/en/rest/repos/contents

### Inferred

The following conclusions follow from the verified mechanics but are architecture judgments rather than documented platform guarantees:

- A local archive path or seekable file object is sufficient to satisfy the current mapper's structural information needs without extraction.
- Avoiding extraction removes the main filesystem-traversal/write hazard but does not remove decompression/resource-exhaustion risk.
- Remote URLs are portable as references but not as guaranteed acquisition mechanisms.
- Opaque runtime handles require adapters before standard archive code can use them.
- A single common archive prefix is evidence of a wrapper but not conclusive proof.
- Archive membership should be treated as snapshot semantics, not automatically as Git-index semantics.

### Proposed

The implementation recommendations in this report are proposals for the larger architecture decision:

- First support local directories, direct ZIP, and direct TAR-family archives.
- Keep archive inspection read-only and non-extracting.
- Normalize only validated relative logical paths.
- Bound member enumeration and selected content reads.
- Refuse to follow links or reproduce special filesystem members.
- Reject duplicate canonical paths by default.
- Use conservative wrapper-root detection with an explicit future override.
- Label archive inventory separately from Git-tracked inventory.
- Make archive readers accept seekable binary file objects internally even if the initial CLI accepts paths.
- Treat remote URLs, provider IDs, and opaque runtime artifacts as adapter-bound inputs rather than core acquisition responsibilities.
- Defer network acquisition, provider integration, archive extraction, and complex Git semantics until the provider-runtime and architecture branches select the external responsibility boundary.
