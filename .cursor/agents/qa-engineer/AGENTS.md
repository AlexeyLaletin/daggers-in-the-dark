# QA Engineer Agent

**Purpose:** QA-specific testing guidelines and quality gates.

**When to use:** When writing or reviewing tests, setting up quality gates.

## QA-Specific Testing Guidelines

### Test Design for QA
- **MUST**: Write tests before fixing bugs (reproduce bug in test)
- **MUST**: Review test code as carefully as production code
- **SHOULD**: Document why tests exist (especially complex ones)
- **SHOULD**: Use appropriate test types for the situation

See Shared Patterns Agent for general testing principles (test organization, quality, coverage, mocking).

## Test Data Management

### Test Fixtures
- **MUST**: Create reusable test fixtures
- **SHOULD**: Use factories for test data generation
- **MUST**: Clean up test data after tests
- **MUST**: Use appropriate test data (not production data)
- **SHOULD**: Document test data requirements

## Quality Gates

### Pre-Commit Checks
- Run linters
- Run type checkers
- Run unit tests
- Check test coverage
- Validate code style

### CI/CD Checks
- Run full test suite
- Run integration tests
- Run e2e tests (on schedule, not every commit)
- Check test coverage thresholds
- Run performance tests

### Code Review Checklist
- Are tests comprehensive?
- Are tests maintainable?
- Is test data appropriate?
- Are mocks used correctly?
- Do tests follow naming conventions?

## Test Maintenance
- Keep tests up-to-date with code changes
- Remove obsolete tests
- Refactor tests when they become hard to maintain
- Document complex test scenarios
- Review test failures carefully

## Test Tools

### Python Testing
- **MUST**: Use `pytest` for testing framework
- **SHOULD**: Use `pytest.fixture` for test fixtures
- **SHOULD**: Use `pytest.parametrize` for multiple test cases
- **SHOULD**: Use `pytest.mock` for mocking
- **SHOULD**: Use `pytest-cov` for coverage
- Commands: `.cursor/rules/reference/commands.mdc`

### C++ Testing
- **SHOULD**: Use appropriate C++ test framework
- **SHOULD**: Use test fixtures for setup/teardown
- **SHOULD**: Mock external dependencies
- **SHOULD**: Use test data generators
- **MUST**: Run tests using the repo’s standard command (the same one CI uses)
