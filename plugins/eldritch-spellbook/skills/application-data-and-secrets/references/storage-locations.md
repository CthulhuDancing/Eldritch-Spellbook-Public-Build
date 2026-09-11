# Storage Locations

Read when selecting or changing an application directory. These are fallback
choices, not a reason to retrofit an established safe deployment. Resolve
paths using the target platform/runtime, not the agent's sandbox or current
working directory.

## Windows

- For a per-user application, use its resolved LocalApplicationData directory
  for machine-local application state.
- For service or machine-shared state, consider the resolved CommonApplicationData
  directory (normally `%ProgramData%`).
- Under the selected root, use stable owner/app/environment names; distinguish
  instances where development copies must not share mutable state. Do not
  hardcode a drive or substitute the agent's profile for the service account.

These categories follow [Microsoft's known folders](https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid).
The folder name alone does not establish protection: inspect effective access
and inheritance on the specific child directory. Give the runtime only needed
read or write access; keep credential/configuration access separate from
runtime-writable data when practical. Never grant broad user access or change
permissions on the whole ProgramData tree as a shortcut.

## Linux and other XDG-based user environments

For a per-user process, use absolute configured XDG bases, with the standard
fallbacks: `~/.config` for configuration, `~/.local/share` for data,
`~/.local/state` for persistent state such as logs, and `~/.cache` for
rebuildable cache. Add application/environment scoping where needed. Resolve
the actual user's home; relative XDG values are invalid. See the
[XDG specification](https://specifications.freedesktop.org/basedir/latest/).

## macOS

Use platform directory APIs and the appropriate user or system domain:
Application Support for application-managed persistent files, Caches for
rebuildable data, and the platform preferences facility for ordinary
preferences. Respect an application's sandbox/container locations rather than
forcing an unrestricted path. See [Apple's filesystem guidance](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html).

## Services, containers, and hosted applications

Follow the existing service manager or hosting platform's configuration,
secret-injection, and persistent-volume contracts. Do not apply interactive-user
directories blindly, put persistent state in an ephemeral image, or bake live
secrets into build artifacts. Keep generic path/variable contracts in the
repository and actual deployment roots in scoped local/operator guidance.

Across platforms, resolve the exact target and inspect existing contents,
ownership, and access before creating or migrating. Keep private exports,
backups, and logs protected too. Reuse compatible download caches separately
from application databases; sharing tools does not mean sharing live data.
If the intended root needs privileges the task lacks, report/use the approved
access path rather than silently changing the application's storage contract.
