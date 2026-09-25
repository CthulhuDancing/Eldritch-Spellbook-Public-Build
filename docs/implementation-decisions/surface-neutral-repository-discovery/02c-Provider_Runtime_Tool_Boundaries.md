# Provider Runtime Tool Boundaries

## Inputs Reviewed

This report was prepared on **2026-09-25** against current first-party documentation for OpenAI/ChatGPT/Codex, Anthropic/Claude/Claude Code, and the Model Context Protocol (MCP). It also uses the project intent as the architectural constraint set: repository normalization must stay outside model context, the mapper should remain deterministic, remote credentials should not be embedded in repository data or prompts, and provider-specific integration should not become part of the structural-analysis core.

The supplied `Intent.md` establishes that `map_repo.py` currently assumes an already-materialized local directory, directly reads structural files from that filesystem, and performs no network access. It also explicitly leaves the remote-acquisition boundary unresolved among script-owned acquisition, runtime-owned acquisition, and a hybrid adapter model. The target outcome is source reference -> deterministic processing -> compact structural output, without the model reconstructing the repository itself.

Research scope:

- OpenAI ChatGPT GitHub connector behavior and Codex/agent execution models.
- OpenAI hosted shell, Agent environments/files, sandbox-agent repository mounts, MCP connections, Plugins/Skills guidance, and Programmatic Tool Calling.
- Anthropic Claude GitHub integration, Claude Code cloud repository setup, Claude Code sandboxing, server-side code execution, Files API, Programmatic Tool Calling, Managed Agents GitHub mounting, and Managed Agents MCP behavior.
- Current MCP concepts for tools/resources and what the protocol does and does not standardize about local filesystem materialization.

All consequential platform claims below are based on first-party documentation unless explicitly labeled as architectural inference.

## Executive Finding

The most portable boundary is **not** to make `map_repo` itself responsible for provider-native remote access. The provider-neutral mapper should consume a normalized repository source that deterministic code can inspect locally or through a small neutral interface. **Acquisition should be a separate adapter/runtime responsibility.**

Current provider models strongly support that separation:

- OpenAI hosted code has no outbound network by default; network can be enabled only through explicit policy. OpenAI's Skills guidance separates deterministic scripts from MCP-backed live data/authentication/actions. [OAI-SHELL] [OAI-SKILLS]
- Anthropic's server-side code execution has internet access disabled, while Claude Code and Managed Agents arrange repository/network access through runtime-controlled mechanisms. [ANT-CODE-EXEC] [ANT-CLAUDE-CLOUD] [ANT-MANAGED-GITHUB]
- Both providers now have mechanisms that can keep large external data out of ordinary model context, but the mechanisms are provider-specific: OpenAI can mount/fetch repositories into agent workspaces and can programmatically process tool results before context; Anthropic can mount GitHub repositories into Managed Agent sandboxes, upload files directly into code-execution containers, and spill large MCP results to sandbox files. [OAI-SANDBOX] [OAI-PTC] [ANT-FILES] [ANT-MANAGED-MCP]
- Neither provider documents a universal rule that a generic chat connector result is automatically exposed as a filesystem object to arbitrary Python. That handoff must be treated as an explicit capability, not assumed.

Therefore, the recommended boundary is:

```text
model / agent
    |
    | source reference + intent
    v
provider/runtime acquisition adapter
    |  owns connector/tool invocation, network policy, credentials
    |  and materialization when the runtime supports it
    v
provider-neutral repository input
    |  local directory, archive, mounted workspace, or neutral repository view
    v
deterministic mapper
    |  no provider SDK dependency; no required remote credentials
    v
compact structural report
    v
model / agent
```

A second valid path is to perform **acquisition and mapping together outside the model sandbox** in a coarse-grained MCP/application service, e.g. `map_repository(repo_ref)`, returning only the compact structural map. That can preserve context isolation when no provider-native filesystem handoff exists. The important boundary is that the model should orchestrate the operation, not reconstruct the repository.

Direct HTTP/GitHub API support may be useful as **one optional acquisition adapter** for environments with approved egress, but making it part of the core `map_repo` contract would create avoidable coupling to network policy, authentication, hosting APIs, rate limits, and provider sandbox behavior.

## OpenAI

### Code Runtime and Networking

OpenAI's current hosted shell documentation states that hosted containers have **no outbound network access by default**. Network can be enabled only when the organization has configured an allowed-domain policy and the request explicitly supplies a compatible `network_policy`; the documentation uses GitHub as an example of a domain that can be permitted. [OAI-SHELL]

This means a deterministic helper running in the hosted shell cannot be designed on the assumption that `git clone`, `urllib`, `requests`, or the GitHub API will work. They may work in a specifically configured environment, but that is a deployment capability, not a portable baseline.

OpenAI's agent architecture also distinguishes the **agent harness/control plane** from the **execution environment**. The harness owns the agent loop, tool routing, approvals, state, and related orchestration, while commands and files operate in an environment. Remote MCP can be invoked without requiring a shell environment, whereas shell/workspace-file execution requires one. [OAI-AGENT-ARCH]

OpenAI's Programmatic Tool Calling runtime is even narrower: its JavaScript execution environment is isolated and does not provide Node.js, package installation, general filesystem access, subprocesses, or direct network access. External access occurs only through enabled tools. [OAI-PTC]

**Implication:** OpenAI supports code that can access the network under explicit policy, but provider-native tool access and ordinary network access are separate capabilities. A Python script does not gain connector/MCP access merely because the model can call those tools.

### Connectors and Repository Access

The ChatGPT GitHub connector is a **read-only, on-demand retrieval integration**. ChatGPT forms searches based on the user's request and retrieves permitted repository content from GitHub. OpenAI explicitly notes that this does not create a continuously synchronized GitHub index. For editing/pushing code, OpenAI directs users to Codex rather than the read-only ChatGPT connector. [OAI-CHATGPT-GITHUB]

That behavior is appropriate for conversational retrieval, but OpenAI's public GitHub-connector documentation does **not** state that the connector creates a local repository checkout or exposes its complete result as a filesystem tree to an arbitrary skill script. Therefore it should not be treated as a documented connector-to-Python handoff.

For agent runtimes, OpenAI documents stronger acquisition primitives. Sandbox Agents can declare a **Git repository to fetch into the workspace**, alongside other storage mounts. OpenAI specifically recommends mounting large data into the sandbox instead of pasting it into model context when file-based work is appropriate. [OAI-SANDBOX]

This is much closer to the desired repository-discovery architecture: acquisition occurs as part of runtime/environment setup, while deterministic code operates on the resulting workspace.

OpenAI's current Plugins/Skills documentation also defines a useful responsibility split. Skills can include `scripts/` for deterministic computation and file processing, while an MCP server is the component that provides live data, authentication, authorization, and actions. [OAI-SKILLS] [OAI-PLUGIN-MCP]

That guidance does not prohibit a script from making HTTP calls in a permissive environment, but it does argue against making provider-authenticated live service access a hidden responsibility of a skill's deterministic helper.

### File/Artifact Handoff

OpenAI's Agents API provides explicit environment file mechanisms. Files can be inserted into an execution environment from OpenAI Files API objects or inline bytes at a chosen workspace path. Files created under the documented output directory can become downloadable artifacts. [OAI-ENV-FILES]

This is a supported **application/runtime -> filesystem -> deterministic code** handoff that does not require the model to receive the file contents as natural-language context first.

Sandbox Agents similarly support workspace mounts, including a Git repository source. [OAI-SANDBOX]

Programmatic Tool Calling provides another context-isolation mechanism, but it is conceptually different. The model can generate orchestration code that invokes eligible tools and processes their results before deciding what enters model context. OpenAI currently lists MCP tools, function/custom tools, shell, code interpreter, and related tools among the supported programmatic-tool categories. OpenAI also emphasizes that programmatic orchestration does not change where the underlying tool executes. [OAI-PTC]

Therefore:

- **Yes:** OpenAI can keep large intermediate tool results from being fully inserted into model context.
- **Yes:** OpenAI can place application-supplied files or repositories in an agent workspace for deterministic code.
- **No documented generic rule:** a normal ChatGPT connector result automatically becomes a local file tree usable by any Python helper.

### Tool Invocation Boundary

OpenAI documents multiple MCP connection origins. A remote HTTP MCP connection can run from the OpenAI service, while environment-origin HTTP or stdio MCP operates from the session environment. Credential exposure differs by origin: service-side connections can use managed credential storage, whereas environment-local processes may receive credentials in environment variables that code in that environment can potentially read. [OAI-MCP]

This directly answers whether connectors/tools run outside the code sandbox: **sometimes**. It depends on the tool's connection/execution origin. The architecture must not collapse “tool” and “sandbox process” into one security domain.

Programmatic Tool Calling permits provider-managed orchestration code to call eligible tools, including MCP, but this should not be confused with granting an arbitrary deterministic Python helper a Python API for invoking ChatGPT's connector registry. The former is part of the agent harness; the latter is not documented as a general skill-script capability. [OAI-PTC]

For the repository mapper, OpenAI's documented model therefore favors either:

1. runtime/application materialization of a repository or archive into the workspace, followed by local deterministic mapping; or
2. an external tool/MCP operation that performs acquisition and returns a compact result.

Embedding ChatGPT connector invocation inside `map_repo.py` would not match a documented portable execution boundary.

## Anthropic

### Code Runtime and Networking

Anthropic's server-side code execution tool runs Python and Bash in an isolated container and documents that **internet access is disabled**. The workspace is intended for uploaded/generated files, not arbitrary outbound fetching. [ANT-CODE-EXEC]

This is a decisive portability constraint: code intended to run inside Claude's provider-managed code-execution container cannot depend on direct GitHub HTTP access.

Claude Code is different because it is an agent/runtime product with an explicit sandbox and network policy. Anthropic documents OS-level sandboxing for shell commands and their child processes, with network access mediated by domain controls and permission behavior. Administrators can use stricter settings to prevent fallback to unsandboxed execution. [ANT-SANDBOX]

Claude Code cloud sessions go further by having the runtime arrange repository access. The cloud environment clones the selected GitHub repository/branch, or can package and upload a local Git repository when appropriate. Anthropic states that Git credentials are kept outside the sandbox and are applied by a scoped proxy rather than handed to agent-generated code. [ANT-CLAUDE-CLOUD]

Anthropic's engineering documentation describes the same broader pattern: network access is proxied, and Git/MCP credentials can remain outside the agent sandbox. [ANT-ENG-SANDBOX] [ANT-ENG-MANAGED]

**Implication:** Anthropic does not provide one universal network rule across every product, but its provider-managed code runtime has no egress, while its agent products put acquisition/network/authentication under runtime policy rather than assuming scripts have unrestricted access.

### Connectors and Repository Access

Claude's ordinary GitHub integration for chats is context-oriented. The user selects repository files/folders, and Claude accesses their names and contents to inform the conversation; project use adds selected repository material to project knowledge. Anthropic also notes context-window limits for this workflow. [ANT-CHAT-GITHUB]

That is not the desired mechanism for deterministic whole-repository structural discovery because repository content is being selected for model use.

Claude Code cloud instead uses a filesystem-centered model: the cloud VM clones the GitHub repository into the session environment before the agent works with it. [ANT-CLAUDE-CLOUD]

Anthropic's newer Managed Agents documentation is even more explicit: a GitHub repository can be **mounted into the session sandbox**, while GitHub MCP can separately be connected for pull-request/action workflows. The repository is available under the workspace filesystem, and repository credentials are handled by the runtime rather than exposed to the agent. [ANT-MANAGED-GITHUB]

That separation maps cleanly to the current design problem:

- Git/repository acquisition can be runtime-managed.
- The mapper can operate against the mounted tree as ordinary deterministic code.
- GitHub action APIs/MCP can remain a separate capability rather than becoming part of the mapper.

### File/Artifact Handoff

Anthropic's Files API can upload a file once and refer to it by `file_id`. For code execution, a `container_upload` content block can place an uploaded file into the code-execution environment. Files generated by code execution or Skills can also be returned as downloadable artifacts. [ANT-FILES]

This is a documented **external/application file -> sandbox file** handoff that avoids requiring the model to reproduce the file text.

Managed Agents provide an additional, particularly relevant MCP handoff. Anthropic documents that when an MCP tool result exceeds 100,000 characters, the result is automatically written to a file in the sandbox; the model receives a truncated preview and a path rather than the full result. [ANT-MANAGED-MCP]

That proves that at least one Anthropic-native agent runtime can bridge an external MCP tool result to deterministic sandbox code without injecting the entire result into model context.

However, this is a **Managed Agents behavior**, not a general MCP guarantee and not necessarily the right repository transport format. Returning a repository as one enormous MCP text result merely to trigger spill-to-file would be inferior to a repository mount, archive file, or coarse-grained mapping operation.

### Tool Invocation Boundary

Anthropic's tool documentation distinguishes **client tools**, which execute in the calling application, from **server tools**, which execute on Anthropic infrastructure. Server tools include Anthropic's MCP connector and code execution. [ANT-TOOL-OVERVIEW]

Anthropic's Programmatic Tool Calling lets Claude generate Python that invokes configured tools while processing large intermediate results outside normal model context. Crucially, the current documentation states that **MCP connector tools cannot be called programmatically** from this code-execution mechanism. It also explains that when a self-managed sandbox has no egress and a tool needs external resources, the application needs a protocol for executing that tool call outside the sandbox. [ANT-PTC]

This is the clearest current example of the distinction the architecture must preserve:

```text
Claude can ask an MCP connector to do something
```

is **not equivalent to**:

```text
a Python helper running in Claude's code sandbox can directly invoke that MCP connector
```

Anthropic does support programmatic invocation of eligible custom/client tools, with the outer application executing those calls and returning results to the suspended code. That is an orchestration bridge owned by the API/runtime, not a normal network capability available to the helper process. [ANT-PTC]

Accordingly, a portable `map_repo` should not assume it can import or call Anthropic's connector/tool layer from Python.

## MCP and External Tooling

MCP standardizes how an AI host/client interacts with servers exposing **tools, resources, and prompts**. Current MCP resources are identified by URI and can return text or binary data. [MCP-SDK] [MCP-RESOURCES]

MCP does **not** standardize that a returned resource becomes a mounted file in the host's execution sandbox. That is a host/runtime policy and implementation decision. Anthropic Managed Agents' large-result spill-to-file is an example of such a provider-specific bridge, not a protocol property. Likewise, OpenAI's environment files and sandbox mounts are OpenAI runtime concepts, not MCP semantics.

For repository acquisition, MCP can solve the context problem effectively if the server exposes an operation at the right granularity. A strong pattern is:

```text
map_repository(repository_reference, options)
    -> compact deterministic structural report
```

The MCP service owns remote Git access, credentials, rate limiting, and the acquisition mechanism. It can invoke the same provider-neutral mapping library/server-side implementation. Only the compact structural result needs to enter the agent flow.

A weaker pattern is to expose only low-level tools such as `list_repository_paths` and `read_repository_file` and expect the model to repeatedly invoke them to reconstruct structure. That reproduces the failure mode identified in the project intent: the agent becomes the normalizer and consumes excessive context/tool turns.

An MCP resource can also represent an archive or repository inventory, but portability still requires an explicit host/application step if deterministic local code must read it. A URI is not automatically a POSIX/Windows path.

## Cross-Provider Comparison

| Question / capability | OpenAI | Anthropic | Portable conclusion |
|---|---|---|---|
| **1. Can provider-hosted code normally make arbitrary outbound requests?** | Hosted shell: no outbound network by default; explicit allowlisting can enable it. PTC JS has no direct network. [OAI-SHELL] [OAI-PTC] | Server-side code execution: internet disabled. Claude Code sandbox/network policies can allow controlled access. [ANT-CODE-EXEC] [ANT-SANDBOX] | Do not make remote network access a required property of mapper code. |
| **2. Typical sandbox network restriction** | Default deny/explicit policy for hosted shell; tool execution origin matters. [OAI-SHELL] [OAI-MCP] | Code execution has no internet; Claude Code uses proxied/allowlisted controls. [ANT-CODE-EXEC] [ANT-SANDBOX] | Treat egress as runtime policy, not library behavior. |
| **3. Expected GitHub access** | ChatGPT GitHub connector for read-only conversational retrieval; Codex/agent environments can use runtime repository/workspace mechanisms. [OAI-CHATGPT-GITHUB] [OAI-SANDBOX] | Chat integration for selected content; Claude Code cloud clones repos; Managed Agents mounts GitHub repos. [ANT-CHAT-GITHUB] [ANT-CLAUDE-CLOUD] [ANT-MANAGED-GITHUB] | Prefer runtime-managed repo materialization for deterministic code. |
| **4. Do connectors/tools run outside the model code sandbox?** | Some do: service-origin remote MCP runs from OpenAI service; environment/stdio MCP can run in the sandbox. [OAI-MCP] | Server tools/MCP connector run on Anthropic infrastructure; client tools run in caller application. [ANT-TOOL-OVERVIEW] | “Tool” is not one execution/security domain; adapter must know origin. |
| **5. Can tool data reach deterministic code without full model ingestion?** | Yes in supported paths: workspace files/mounts; PTC can process eligible tool outputs before context. No generic ChatGPT-connector-to-Python mount is documented. [OAI-ENV-FILES] [OAI-SANDBOX] [OAI-PTC] | Yes: file uploads to code container, repo mounts, PTC for eligible client tools, Managed Agents MCP spill-to-file. MCP connector itself is excluded from PTC. [ANT-FILES] [ANT-MANAGED-GITHUB] [ANT-PTC] [ANT-MANAGED-MCP] | Capability exists, but the handoff mechanism is provider/runtime-specific. |
| **6. Mounted/files/artifacts/resources concepts** | Environment files, Files API IDs, workspace artifacts, Git repo/storage mounts, MCP resources/tools. [OAI-ENV-FILES] [OAI-SANDBOX] | Files API, `container_upload`, generated artifacts, Managed Agent GitHub mounts, MCP result files. [ANT-FILES] [ANT-MANAGED-GITHUB] [ANT-MANAGED-MCP] | Normalize these into local/archive/repository-view inputs behind adapters. |
| **7. Boundary for credentials** | Service-side MCP can use managed credential storage; environment-side credentials may be visible to code depending on configuration. [OAI-MCP] | Claude Code/Managed Agents document credential proxies/vaulting outside agent sandbox. [ANT-CLAUDE-CLOUD] [ANT-ENG-MANAGED] | Keep repository credentials in runtime/acquisition layer, not mapper API or model context. |
| **8. Should deterministic helper invoke provider tools directly?** | Skills docs separate deterministic scripts from MCP live data/auth/actions; PTC tool invocation belongs to agent harness. [OAI-SKILLS] [OAI-PTC] | PTC explicitly demonstrates outer application executing tool calls; MCP connector unavailable to sandbox PTC. [ANT-PTC] | No portable basis for helper-owned provider-tool invocation. Orchestration belongs outside core mapper. |
| **9. Can MCP keep raw repo out of model context?** | Yes if an external MCP service performs acquisition/mapping or PTC filters results; generic filesystem handoff is not guaranteed. [OAI-PTC] | Yes if external MCP performs acquisition/mapping; Managed Agents can spill large MCP results to sandbox files. [ANT-MANAGED-MCP] | Prefer coarse-grained acquire+map service, not model-driven low-level traversal. |
| **10. Architecture resilient to provider differences** | Provider adapter -> workspace/repo view -> neutral mapper, or external acquire+map tool. | Same. | Put provider differences at acquisition/materialization boundary. |
| **11. Direct HTTP/GitHub API in `map_repo` portable?** | Only where egress/network policy permits; connector credentials are separate. | Fails in server-side code execution and depends on Claude Code policy elsewhere. | No as a core requirement. Acceptable only as an optional adapter. |
| **12. Provider-specific acquisition adapter around neutral mapper?** | Fits workspace files/mounts, plugin/MCP responsibility split. | Fits repo mounts, Files API, tool/application separation. | Yes; best alignment with both documented platform models. |

## Portable Architectural Implications

1. **The structural mapper should not own provider credentials or connector authentication.** Both vendors have runtime-managed credential models, and both distinguish the tool/control plane from code execution. Moving credentials into `map_repo` would bypass those controls and create deployment-specific secret handling.

2. **The mapper should not require outbound network access.** Network availability ranges from disabled to explicitly allowlisted to runtime-proxied. A mapper with mandatory GitHub HTTP behavior would fail in legitimate first-party runtimes.

3. **Repository acquisition and repository analysis should be separate contracts.** The acquisition side may be implemented by a Git clone, provider GitHub mount, uploaded archive, Files API upload, remote MCP service, or future artifact handle. The mapping side should see only a normalized repository view.

4. **A local/mounted filesystem is a good optimization, not the only abstraction.** Both providers now have first-party paths that materialize files/repositories into a sandbox. The neutral interface should still allow an archive or virtual repository view so the design does not become coupled to filesystem extraction.

5. **Provider tool orchestration should remain outside mapper code.** OpenAI PTC and Anthropic PTC show that tool invocation can be embedded in provider-managed orchestration code, but their capabilities differ materially. That is evidence for keeping such orchestration in a provider adapter/harness layer rather than treating it as a feature of the mapper.

6. **If no file handoff exists, move acquisition+mapping outward rather than moving normalization into the model.** An application service or MCP server can acquire the repository and return the compact structural report. This preserves the model-context requirement without depending on sandbox egress.

7. **Prefer coarse-grained external operations.** `map_repository(ref)` is more context-efficient and deterministic than repeated `list/read/search` calls whose outputs the model must assemble.

## Approaches That Create Provider Lock-In

### Putting provider connector calls inside `map_repo`

This would couple the mapper to a provider's tool registry, execution protocol, authentication model, and tool-call lifecycle. OpenAI's and Anthropic's programmatic tool mechanisms are not API-compatible and do not expose identical eligible tools. Anthropic currently excludes MCP connector tools from PTC, while OpenAI permits MCP among eligible PTC tools. [OAI-PTC] [ANT-PTC]

### Requiring direct GitHub HTTP from mapper code

This assumes outbound egress, DNS, TLS, GitHub availability, credentials, and API semantics. Those assumptions are false for Anthropic server-side code execution and false by default for OpenAI hosted shell. [ANT-CODE-EXEC] [OAI-SHELL]

### Depending on a provider-specific sandbox path

OpenAI and Anthropic both expose workspace/container files, but path conventions and lifecycle differ. A provider adapter can convert the provider object/mount into the mapper's neutral input without making the core depend on `/workspace`, `/mnt/data`, or another provider-owned path convention.

### Assuming all connector outputs become local files

This is not documented as a cross-provider capability. Anthropic Managed Agents have one documented large-MCP-result spill-to-file behavior; OpenAI has explicit environment-file APIs and mounts, but the normal ChatGPT GitHub connector is documented as conversational retrieval rather than automatic workspace materialization. [ANT-MANAGED-MCP] [OAI-CHATGPT-GITHUB] [OAI-ENV-FILES]

### Using low-level connector retrieval as the normalization algorithm

Even where technically possible, this makes the model/harness iterate through repository paths and selected files. That reintroduces the context/tool-turn overhead the mapper exists to prevent.

## Recommended Responsibility Boundary

**Recommendation: use a provider-specific acquisition adapter around a provider-neutral deterministic repository mapper.**

The responsibilities should be:

### Agent/model

- Identify or receive the source reference.
- Select the appropriate acquisition capability exposed by its runtime.
- Request structural mapping.
- Receive only the compact structural result plus deliberately requested follow-up files.
- Do **not** enumerate/reconstruct the repository as an intermediate representation.

### Provider/runtime acquisition adapter

- Own provider-native connector/tool invocation.
- Own network policy and remote repository acquisition.
- Keep credentials in the provider/application's supported secret mechanism.
- Prefer a direct repository mount, workspace file, uploaded archive, or other provider-managed artifact when available.
- Convert provider-specific handles into one neutral input form for deterministic processing.
- If local materialization is unavailable, call an external coarse-grained acquisition+mapping service and return its compact result.

### Deterministic repository mapper

- Own structural classification only.
- Accept a local directory, archive-native source, or neutral repository inventory/read interface.
- Read only structural metadata needed for mapping.
- Require no provider SDK.
- Require no connector registry.
- Require no remote credentials.
- Require no network access for its core behavior.

### Optional network acquisition adapter

A direct Git/HTTP/GitHub implementation can still exist, but it should be an **optional source adapter**, e.g. conceptually:

```text
RemoteGitAdapter      # direct git/API when runtime policy permits
OpenAIWorkspaceAdapter
AnthropicWorkspaceAdapter
ArchiveAdapter
LocalDirectoryAdapter
ExternalMCPMapAdapter
        |
        v
RepositoryView / normalized inventory
        |
        v
map_repo core
```

This keeps direct network support useful in local/CI/self-hosted environments without making it a requirement of provider-hosted execution.

### Preferred provider-native paths

- **OpenAI agent environment:** runtime fetch/mount repository or place an uploaded archive/file in the environment; run mapper locally. [OAI-SANDBOX] [OAI-ENV-FILES]
- **Anthropic Managed Agents / Claude Code cloud:** runtime mounts/clones repository; run mapper locally. [ANT-MANAGED-GITHUB] [ANT-CLAUDE-CLOUD]
- **OpenAI/Anthropic environment without repository mounting but with application file upload:** application acquires an archive outside the sandbox, uploads it into the environment, mapper inspects the archive directly. [OAI-ENV-FILES] [ANT-FILES]
- **Environment with only external tools/MCP:** external service performs repository acquisition and ideally mapping, returning the compact map. Do not require the model to relay raw repository contents.

This boundary is the smallest one that remains correct across the documented capability differences as of 2026-09-25.

## Documentation Gaps

1. **ChatGPT connector -> arbitrary skill-script file handoff:** OpenAI documents GitHub retrieval for ChatGPT, but the public connector documentation reviewed does not specify a general mechanism by which a normal connector result becomes a filesystem object readable by a skill's Python script without model mediation.

2. **Generic OpenAI MCP result -> environment file:** OpenAI documents MCP invocation, programmatic tool processing, environment files, and mounts separately. The reviewed documentation does not establish a universal automatic MCP-result-to-workspace-file bridge analogous to Anthropic Managed Agents' documented large-output spill behavior.

3. **Claude chat GitHub -> code-execution filesystem:** Anthropic documents selected GitHub content for chats and separate Files/code-execution mechanisms, but the reviewed ordinary-chat integration docs do not state that selected repository content is automatically mounted for arbitrary deterministic code.

4. **Cross-provider artifact-handle standard:** Neither provider exposes a common artifact/file-handle API that a portable Python helper can consume directly. MCP resources are protocol-level resources, not standardized local file descriptors or paths.

5. **Provider-native scripts invoking provider tools:** Both vendors document harness/application mechanisms for tool execution, but neither reviewed documentation describes a provider-neutral API whereby an arbitrary deterministic script inside the sandbox can enumerate and invoke the host's connector registry as ordinary library calls.

6. **Lifecycle/performance guarantees:** Repository mount/cache lifetime, maximum practical repository size, and exact file-transfer thresholds vary by product and may be beta behavior. These should be treated as adapter concerns rather than core mapper guarantees.

## Unresolved Questions

These questions remain implementation-specific rather than blockers for the responsibility decision:

- Which OpenAI surface will `efficient-codebase-discovery` target in normal ChatGPT use, and does that surface expose repository/workspace materialization to installed Skills in the same way the Agents SDK/Sandbox Agents API does?
- Whether an OpenAI ChatGPT plugin/Skill can receive a connector-created file handle directly in its script environment is not established by the reviewed public documentation.
- Whether Anthropic Managed Agents' GitHub mount and large-MCP-output file behavior will remain stable when those beta features graduate.
- Whether an external MCP `map_repository` service should return only the compact map, or also return a provider-neutral artifact/resource reference for later targeted reads.
- What repository-size and transfer limits should the acquisition adapter enforce before choosing clone, archive upload, or server-side mapping.
- Whether direct Git support should be shipped at all in the first iteration or added only after local/archive/provider-mounted sources are working. The platform evidence supports it only as an optional adapter, not as a core dependency.

## Sources

### OpenAI

- **[OAI-CHATGPT-GITHUB]** OpenAI Help Center, “Connecting GitHub to ChatGPT,” current page retrieved 2026-09-25. <https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt>
- **[OAI-SKILLS]** OpenAI Developers, “Skills – Plugins” / skill concepts, current documentation retrieved 2026-09-25. <https://developers.openai.com/plugins/concepts/skills>
- **[OAI-PLUGIN-MCP]** OpenAI Developers, Plugins / MCP server guidance, current documentation retrieved 2026-09-25. <https://developers.openai.com/plugins>
- **[OAI-SHELL]** OpenAI Developers, “Shell,” hosted-shell networking and containers, current documentation retrieved 2026-09-25. <https://developers.openai.com/api/docs/guides/tools-shell>
- **[OAI-PTC]** OpenAI Developers, “Programmatic Tool Calling,” current documentation retrieved 2026-09-25. <https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling>
- **[OAI-AGENT-ARCH]** OpenAI Developers, Agents API architecture, current documentation retrieved 2026-09-25. <https://developers.openai.com/api/docs/guides/agents-api/architecture>
- **[OAI-MCP]** OpenAI Developers, Agents API MCP connections, current documentation retrieved 2026-09-25. <https://developers.openai.com/api/docs/guides/agents-api/tools/mcp>
- **[OAI-SANDBOX]** OpenAI Developers, Agents SDK / Sandbox Agents, current beta documentation retrieved 2026-09-25. <https://developers.openai.com/api/docs/guides/agents/sandboxes>
- **[OAI-ENV-FILES]** OpenAI Developers, Agents API environment files, current documentation retrieved 2026-09-25. <https://developers.openai.com/api/docs/guides/agents-api/environments/files>

### Anthropic

- **[ANT-CHAT-GITHUB]** Anthropic Support, “Use the GitHub integration,” current documentation retrieved 2026-09-25. <https://support.claude.com/en/articles/10167454-use-the-github-integration>
- **[ANT-CLAUDE-CLOUD]** Anthropic Claude Code Docs, “Use Claude Code in the cloud,” current documentation retrieved 2026-09-25. <https://code.claude.com/docs/en/claude-code-on-the-web>
- **[ANT-SANDBOX]** Anthropic Claude Code Docs, “Sandboxing,” current documentation retrieved 2026-09-25. <https://code.claude.com/docs/en/sandboxing>
- **[ANT-CODE-EXEC]** Anthropic Platform Docs, “Code execution tool,” current documentation retrieved 2026-09-25. <https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool>
- **[ANT-PTC]** Anthropic Platform Docs, “Programmatic tool calling,” current documentation retrieved 2026-09-25. <https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling>
- **[ANT-TOOL-OVERVIEW]** Anthropic Platform Docs, “Tool use overview,” current documentation retrieved 2026-09-25. <https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview>
- **[ANT-FILES]** Anthropic Platform Docs, “Files API,” current documentation retrieved 2026-09-25. <https://platform.claude.com/docs/en/build-with-claude/files>
- **[ANT-MANAGED-MCP]** Anthropic Platform Docs, Managed Agents MCP connector, current beta documentation retrieved 2026-09-25. <https://platform.claude.com/docs/en/managed-agents/mcp-connector>
- **[ANT-MANAGED-GITHUB]** Anthropic Platform Docs, Managed Agents GitHub repository mounting, current beta documentation retrieved 2026-09-25. <https://platform.claude.com/docs/en/managed-agents/github>
- **[ANT-ENG-SANDBOX]** Anthropic Engineering, “Claude Code sandboxing,” published 2025-10-20. <https://www.anthropic.com/engineering/claude-code-sandboxing>
- **[ANT-ENG-MANAGED]** Anthropic Engineering, Managed Agents architecture/security article, 2026 generation, retrieved 2026-09-25. <https://www.anthropic.com/engineering/managed-agents>

### Model Context Protocol

- **[MCP-SDK]** Model Context Protocol, TypeScript SDK v2 documentation implementing the current 2026 protocol generation, retrieved 2026-09-25. <https://ts.sdk.modelcontextprotocol.io/v2/>
- **[MCP-RESOURCES]** Model Context Protocol, resources/client documentation, retrieved 2026-09-25. <https://ts.sdk.modelcontextprotocol.io/v2/get-started/first-client.html>
- Model Context Protocol Blog, 2026-07-28 specification release. <https://blog.modelcontextprotocol.io/posts/2026-07-28/>

## Evidence Classification

### Class A — Direct first-party product/API documentation

Used for the primary capability claims and the recommendation boundary:

- OpenAI hosted-shell networking, Agents API environment files, Sandbox Agents mounts, MCP execution origin, Programmatic Tool Calling, ChatGPT GitHub connector, and Skills/Plugins separation.
- Anthropic code-execution networking, Programmatic Tool Calling restrictions, Files API, Claude Code cloud setup, Claude Code sandboxing, Managed Agents GitHub mount, Managed Agents MCP file spill, and ordinary Claude GitHub integration.
- MCP SDK/spec documentation for protocol-level tools/resources.

These are treated as **documented capabilities**, not assumptions about all product surfaces.

### Class B — First-party engineering implementation descriptions

Anthropic engineering posts are used to clarify how its credential/network proxies isolate secrets from sandboxed agent code. They support the architectural interpretation but are not used to broaden product guarantees beyond the corresponding product docs.

### Class C — Architectural inference from documented capabilities

The following are recommendations, not vendor-prescribed requirements:

- Keep the mapper provider-neutral and network-optional.
- Put connector/tool invocation, credential handling, and remote acquisition in provider/runtime adapters.
- Prefer filesystem/artifact materialization where offered.
- Use an external coarse-grained acquisition+mapping service where materialization is unavailable.
- Keep direct GitHub HTTP/Git support as an optional adapter rather than the mapper's core contract.

These inferences follow from the fact that first-party runtimes differ materially in network access and tool-to-code handoff, while both support runtime/application-owned acquisition paths.

### Evidence intentionally not used

No community reports are required for the recommendation. Where first-party documentation does not specify a generic connector-to-script handoff, this report records the gap rather than inferring one from observed UI behavior or third-party discussion.
