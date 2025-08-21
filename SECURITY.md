# Security Policy

## Secret Management
- Environment variables may be loaded from a local `.env` file during development.
- **Do not store production secrets in `.env` files.** Use a secure secrets vault or key management service instead.
- API keys and other credentials should never be committed to the repository.

## Request Limits
- Global configuration enforces `timeout` and `max_tokens` limits to prevent resource abuse.
- Requests exceeding these limits will be rejected.

## Tool Permissions
- Tool usage is governed by configuration permissions. Disabled tools cannot be invoked.
- Sensitive actions such as `write_file`, `delete_file`, or `execute_command` require explicit user confirmation.

Please report security concerns via the repository issue tracker.
