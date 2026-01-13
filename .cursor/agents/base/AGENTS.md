# Base Agent

**Purpose:** General engineering rules applicable to all roles.

**When to use:** Always follow these base rules regardless of your role.

## Repository Conventions

- Follow the existing repository conventions for naming, layout, and tooling.
- Prefer small, reviewable changes over large rewrites.
- Avoid over-engineering; solve the problem at hand.

## Task Management (Shrimp)

- **MUST**: Use Shrimp Task Manager (MCP) to plan and track multi-step work (2+ steps).
- **MUST**: Keep task statuses updated while implementing; do not finish with open tasks.
- See `.cursor/rules/practices/shrimp_task_manager.mdc`.

## Version Control (Git)

- Prefer a clean, linear history when the repo/team expects it (often via rebase).
- Keep commits focused and messages descriptive.
- Don’t commit generated artifacts unless the repo explicitly requires them.

## Code Organization

- Write self-documenting code - prefer clear names over comments
- Keep functions focused and single-purpose

## Documentation

- **MUST**: Keep documentation up-to-date with code changes
- **SHOULD**: Include examples in documentation
- **SHOULD**: Document "why" not just "what" for complex decisions
- **AVOID**: Comments that just restate the code
- See `.cursor/rules/practices/documentation.mdc` for detailed guidelines
- See `.cursor/rules/practices/llm_filtering.mdc` for comment anti-patterns

## Testing

- Write tests alongside code (TDD preferred)
- Tests should be fast, isolated, and repeatable
- Use appropriate test types: unit, integration, e2e
- Test edge cases and error conditions

## Code Review

- **MUST**: Review your own code before submitting
- **MUST**: Check for common LLM-generated code problems (see `.cursor/rules/practices/llm_filtering.mdc`)
- **MUST**: Ensure code follows project conventions
- **MUST**: Verify tests pass locally before submitting

## Security and Privacy

- **MUST**: Never commit secrets, tokens, or credentials
- **MUST**: Use `.cursorignore` to exclude sensitive files from Cursor context
- **MUST**: Never commit `.env.*`, `*.pem`, or credential files
- **SHOULD**: Review `.cursorignore` file to ensure sensitive data is excluded
- **MUST**: Never include secrets, tokens, credentials, or production configs in Cursor context
- **MUST**: Add project-specific sensitive paths to `.cursorignore`
- See `.cursor/rules/setup/security.mdc` for `.cursorignore` configuration and security best practices
