# Shared Patterns Agent

**Purpose:** Common patterns, anti-patterns, and shared principles applicable to all roles.

**When to use:** Always reference these shared patterns when writing code.

## Common Utility Patterns

### Error Handling
- Use specific exception types, not generic Exception
- Include context in error messages
- Log errors appropriately (not just print)
- Handle errors at appropriate levels

### Logging
- Use structured logging when available
- Include relevant context (request IDs, user IDs, etc.)
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Don't log sensitive information (passwords, tokens, PII)

### Configuration
- Use environment variables for environment-specific config
- Validate configuration on startup
- Provide sensible defaults
- Document configuration options

### Resource Management
- Always close resources (files, connections, etc.)
- Use context managers when available
- Clean up temporary resources
- Handle resource exhaustion gracefully

## Code Organization Patterns

### Module Structure
- One main class/function per module when possible
- Group related functionality together
- Separate concerns (business logic, I/O, validation)
- Use packages to organize larger projects

### Function Design
- Keep functions small and focused
- Limit function parameters (prefer data structures for many params)
- Return early for error cases
- Use descriptive function names

### Class Design
- Single Responsibility Principle
- Prefer composition over inheritance
- Keep classes focused and cohesive
- Use interfaces/protocols for abstraction

## Anti-Patterns to Avoid

### Over-Engineering
- Don't create abstractions before you need them
- Don't optimize prematurely
- Don't add features "just in case"
- Solve the actual problem, not hypothetical ones

### Code Smells
- Long functions (>50 lines is a warning sign)
- Deep nesting (>3 levels is a warning sign)
- Duplicate code (DRY principle)
- Magic numbers (use named constants)
- Commented-out code (remove it or explain why it's kept)

### LLM-Generated Code Issues
- Useless comments that just restate the code
- Overly verbose variable names
- Unnecessary abstractions
- Template code that doesn't fit the context
- Missing error handling
- Inconsistent style with existing codebase

## Testing Principles

### General Testing Rules
- **MUST**: Write tests alongside code (TDD preferred)
- **MUST**: Tests should be fast, isolated, and repeatable
- **SHOULD**: Use appropriate test types: unit, integration, e2e
- **MUST**: Test edge cases and error conditions
- **SHOULD**: Keep tests independent (no test order dependencies)

### Test Types
- **Unit Tests**: Test individual functions/methods in isolation
  - Fast execution (<1 second each)
  - Mock external dependencies
  - Test behavior, not implementation

- **Integration Tests**: Test component interactions
  - Use real dependencies when possible
  - Test data flows
  - Test error propagation

- **End-to-End Tests**: Test complete user workflows
  - Use production-like environment
  - Keep minimal (they're slow)
  - Focus on critical paths

### Test Organization
- **MUST**: Organize tests by feature/component
- **MUST**: Use clear test names that describe what is being tested
- **SHOULD**: Group related tests in test classes/modules
- **MUST**: Separate unit, integration, and e2e tests
- **SHOULD**: Use test fixtures for common setup

### Test Quality
- **MUST**: One assertion per test when possible (or related assertions)
- **MUST**: Test one thing at a time
- **SHOULD**: Use descriptive test names: `test_function_name_should_do_something_when_condition`
- **MUST**: Keep tests simple and readable

### Test Coverage
- **SHOULD**: Aim for meaningful coverage, not just percentage
- **MUST**: Test happy paths
- **MUST**: Test error cases and edge cases
- **SHOULD**: Test boundary conditions
- **SHOULD**: Test integration points

### Mocking Guidelines
- **SHOULD**: Mock external services (APIs, databases)
- **SHOULD**: Mock slow operations (file I/O, network)
- **SHOULD**: Mock non-deterministic behavior (random, time)
- **AVOID**: Over-mocking (test real behavior when possible)
- **AVOID**: Mocking simple data transformations or business logic
