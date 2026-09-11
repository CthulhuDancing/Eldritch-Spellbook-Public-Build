# Credential Handling

Read when integrating or moving credentials, or handling a concrete exposure.

- Prefer the application's supported workload identity, operating-system
  credential facility, or established secret manager. Do not assume one
  user's store can be read by a service account.
- When a file is necessary, keep it outside source/release trees with access
  restricted to the required identities. Environment injection may be
  appropriate but is not inherently confidential: values can escape through
  diagnostics and process dumps.
- Inspect key names and references rather than values. Do not dump entire
  environment/configuration files or pass real secrets in shell arguments.
  Minimize and redact captured logs before sharing them.
- Git ignores prevent some future additions; they do not untrack files,
  cleanse history, or protect published artifacts. Use synthetic placeholders
  in examples and tests. Never put a server credential in browser-delivered
  code or configuration.
- If a real credential is exposed, avoid repeating it, identify the affected
  credential by reference, and report the exposure. Revocation/rotation and
  containment need the owning system's authorized response; moving a file
  alone does not invalidate the leaked credential. Do not rewrite history,
  revoke credentials, or disrupt consumers without that authority.

These safeguards draw on the [OWASP secrets-management guidance](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html).
