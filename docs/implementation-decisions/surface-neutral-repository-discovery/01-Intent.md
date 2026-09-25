# Intent: Runtime-Neutral Repository Discovery

## Stage

Initial intent definition for manual diamond exploration.

## Origin

The `efficient-codebase-discovery` skill currently includes `scripts/map_repo.py`, a deterministic structural repository mapper intended to reduce model context use during codebase discovery.

The current implementation works well when the repository already exists as an accessible local directory. It does not adequately support provider-native chat runtimes where the repository may instead be represented by an uploaded archive, remote repository URL, connector-accessible repository, or another non-filesystem source.

A previous attempt to use the workflow against a large remote repository caused the chat model to perform excessive discovery itself, consuming substantial context rather than delegating structural processing to the deterministic helper. This is the failure mode this design work is intended to prevent.

---

## Verified Current Behavior

Direct inspection of the current `scripts/map_repo.py` establishes the following.

### Input contract

The CLI accepts:

```text
map_repo.py [path]
```

The supplied value is converted to a `Path`.

The script currently requires:

- the path to exist;
- the path to be a directory.

Anything else is rejected before repository mapping begins.

### Repository inventory

For a Git repository, the helper:

1. invokes `git rev-parse --show-toplevel`;
2. invokes `git ls-files -z`;
3. treats Git-tracked files as the authoritative inventory.

If Git inventory is unavailable, it falls back to an `os.walk()` filesystem traversal.

### File access

Structural metadata such as `package.json` hints are obtained by opening files directly beneath the repository root.

The mapper therefore assumes that the repository has already been materialized into a filesystem accessible to the Python process.

### Analysis performed

The helper primarily reports repository **structure**, not source-code meaning.

Its results include information such as:

- repository root;
- inventory source;
- file count;
- manifests;
- manifest-declared entry points;
- navigation files;
- likely source roots;
- candidate code surfaces;
- test roots;
- documentation roots;
- conventional entry-point candidates;
- top-level file distribution;
- file-type distribution.

Its compact format is specifically intended for efficient agent consumption.

### Networking

The current script has no remote-repository acquisition layer and performs no network access itself.

---

## Problem

The discovery workflow becomes inefficient when the runtime can identify a repository but cannot present it as a conventional local directory.

Examples include:

- repository URLs;
- repositories accessible through a provider connector;
- uploaded `.zip`, `.tar`, or similar source archives;
- repositories exposed through future runtime-specific mechanisms.

In those environments, the model may end up manually retrieving, listing, reading, or reasoning over large portions of the repository merely to reconstruct the structural information that `map_repo.py` was designed to provide.

This defeats the purpose of the deterministic helper and can cause excessive token consumption or context exhaustion.

---

## Primary Goal

Allow repository structural discovery to operate across provider-native chat runtimes without requiring the model itself to ingest or normalize the repository.

Ideally the agent should need to provide only a simple source reference such as:

```text
/local/repository/path
```

or:

```text
https://github.com/example/project
```

or an uploaded archive supplied by the runtime.

The deterministic helper layer should perform the mechanical discovery necessary to transform that source into the compact structural evidence needed by the model.

---

## Architectural Direction to Explore

A likely architectural seam is:

```text
Repository source
      │
      ▼
Source acquisition / normalization
      │
      ▼
Normalized repository representation
      │
      ▼
Structural mapping
      │
      ▼
Compact map_repo output
      │
      ▼
Agent reasoning
```

The normalization function may live in:

- a second helper script;
- a reusable Python module;
- adapters within an expanded `map_repo` implementation;
- another architecture identified during exploration.

No specific implementation is selected yet.

The normalization layer should be designed so that additional repository source types can be added later without requiring substantial changes to the structural mapping logic.

---

## Critical Constraint: Agent Context Isolation

The agent itself must **not** be responsible for repository normalization.

An invalid design would require the model to:

1. retrieve repository files;
2. load their contents into its own context;
3. construct a normalized representation;
4. pass that representation to the helper.

That merely moves the existing context-efficiency problem earlier in the workflow.

The desired flow is instead approximately:

```text
Agent supplies source reference
            │
            ▼
Deterministic tooling performs normalization
            │
            ▼
Agent receives compact structural output
```

The repository should remain outside model context except for files deliberately inspected after structural discovery identifies them as relevant.

---

## Archive Requirement

Uploaded source archives should be usable **without extracting their contents to the filesystem** where practical.

Preferred behavior is direct inspection using archive APIs.

Examples may include:

- ZIP central-directory inspection;
- TAR stream/member inspection;
- other safe read-only archive interfaces.

Reasons include:

- cleaner runtime safety boundaries;
- avoiding unnecessary filesystem writes;
- avoiding extraction-path risks;
- reducing environmental assumptions;
- keeping structural discovery deterministic.

The structural mapper generally needs paths and selected manifest metadata rather than complete repository extraction.

---

## Platform Neutrality

The solution should avoid unnecessary dependence on:

- one AI provider;
- one sandbox layout;
- one connector product;
- one authentication mechanism;
- one Git hosting provider;
- provider-specific shell behavior.

Provider-specific adapters may be appropriate, but the core representation and mapping behavior should remain portable.

The architecture should remain useful in:

- local agent runtimes;
- OpenAI native chat runtimes;
- Anthropic/Claude native runtimes;
- other compatible agent environments.

---

## Remote Repository Question

The correct boundary for remote access is intentionally unresolved.

Candidate approaches include:

### Script-owned acquisition

The deterministic helper receives a remote repository reference and performs the necessary API or network operations itself.

### Runtime-owned acquisition

The agent/runtime invokes its available GitHub or repository connector and makes the resulting resource available to deterministic tooling without loading the repository through model context.

### Hybrid adapter model

A source adapter defines an interface that may be backed by HTTP, a connector, a local tool invocation, or another provider mechanism while keeping repository mapping itself independent of those details.

Provider documentation and recommended agent/tool patterns should be examined before selecting among these approaches.

---

## Desired Input Classes

At minimum, exploration should account for:

### Local directory

Existing behavior should continue to work.

### Uploaded archive

The mapper or normalization layer should inspect repository structure directly from the archive without normal extraction.

### Remote Git repository

A simple repository identifier or URL should ideally be sufficient where the runtime provides a viable acquisition mechanism.

### Future adapters

The design should permit additional sources without redesigning the mapper.

Potential examples include:

- provider file objects;
- artifact stores;
- alternate Git hosts;
- object storage;
- pre-generated repository inventories.

These are extensibility targets rather than immediate implementation requirements.

---

## Important Safety Properties

Repository discovery should remain:

- read-only;
- deterministic where possible;
- bounded;
- resistant to path traversal;
- independent of executing repository code;
- independent of installing repository dependencies;
- conservative about network and credential use.

Uploaded archives must not gain arbitrary filesystem-write behavior merely because they contain unusual paths.

Remote repository support must not require embedding credentials into repository data or model context.

---

## Context-Efficiency Requirement

The resulting workflow should preserve the existing purpose of `map_repo.py`.

A successful interaction should resemble:

```text
source reference
      ↓
deterministic processing
      ↓
small structural report
      ↓
targeted source inspection
```

It should not resemble:

```text
source reference
      ↓
model retrieves hundreds or thousands of paths/files
      ↓
model reconstructs repository structure
      ↓
mapper becomes redundant
```

---

## Compatibility Requirement

The existing local-directory workflow should remain simple.

Improving remote and archive support should not make this substantially harder:

```bash
python scripts/map_repo.py /path/to/repository --format compact
```

Backward-compatible CLI behavior is preferred unless a materially better interface justifies a change.

---

## Key Questions

The exploration must determine:

1. What normalized representation should separate repository acquisition from repository structural analysis?

2. Should that representation be an in-memory Python abstraction, serialized format, stream interface, temporary artifact, or something else?

3. How should archives be inspected directly and safely without extraction?

4. What is the simplest input contract that works across local paths, uploaded archives, and remote repositories?

5. Should remote acquisition belong inside deterministic scripts, outside them in provider tooling, or behind a pluggable adapter boundary?

6. What do current OpenAI and Anthropic agent/runtime recommendations imply about scripts initiating network access versus invoking provider tools/connectors?

7. Can provider-native tooling hand data to deterministic code without first putting that data into the model context?

8. How much provider-specific integration is unavoidable?

9. How can future source types be added without coupling them to `map_repo` analysis logic?

10. Can these changes preserve the script's current small, deterministic output and simple local behavior?

---

## Decision to Be Reached

Determine the smallest extensible architecture that allows `efficient-codebase-discovery` to structurally inspect repositories in both local and provider-native chat environments while:

- minimizing model context consumption;
- preserving deterministic structural analysis;
- avoiding unnecessary filesystem writes;
- supporting archive-native inspection;
- remaining as platform-neutral as practical;
- and respecting provider-native networking/tool boundaries.

The final decision should define both:

1. the internal architecture of the helper tooling; and
2. the responsibility boundary between the helper, the agent runtime, and external repository services.

No implementation should begin until these boundaries are sufficiently resolved.