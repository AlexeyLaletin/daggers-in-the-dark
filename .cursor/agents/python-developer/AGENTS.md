# Python Developer Agent

**Purpose:** Python-specific coding standards and best practices.

**When to use:** When writing Python code in this repository.

## Code Style

### Type Hints
- Use type hints for all function signatures
- Use type hints for class attributes
- Prefer `typing` module types over built-in types when needed
- Use `Optional[T]` or `T | None` for nullable types
- Use `Union` for multiple types when needed
- Use generic types (`List[T]`, `Dict[K, V]`) instead of raw types

### Import Organization
- Standard library imports first
- Third-party imports second
- Local imports last
- Use absolute imports, avoid relative imports when possible
- Group imports with blank lines between groups
- Sort imports alphabetically within groups

### Naming Conventions
- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes/methods: `_leading_underscore`
- Module names: `snake_case`

### Docstrings
- Use Google-style or NumPy-style docstrings
- Include: description, args, returns, raises
- Document complex algorithms
- Include examples for public APIs

### Code Structure
```python
# Good structure
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class MyClass:
    """Class description."""

    def __init__(self, param: str) -> None:
        """Initialize with param."""
        self._param = param

    def public_method(self, arg: int) -> Optional[str]:
        """Public method description.

        Args:
            arg: Argument description.

        Returns:
            Optional string result.
        """
        if arg < 0:
            return None
        return str(arg)
```

## Python-Specific Best Practices

### Error Handling
- **MUST**: Use specific exceptions: `ValueError`, `TypeError`, `KeyError`, etc.
- **SHOULD**: Create custom exceptions for domain-specific errors
- **MUST**: Use context managers for resource management
- **SHOULD**: Use `try/except/else/finally` appropriately
- See Shared Patterns Agent for general error handling principles

### Data Structures
- Use `collections` module when appropriate (defaultdict, Counter, etc.)
- Prefer list/dict comprehensions for simple transformations
- Use generators for large datasets
- Use `dataclasses` or `NamedTuple` for structured data

### Testing
- **MUST**: Use `pytest` for testing framework
- **SHOULD**: Use `pytest.fixture` for test fixtures
- **SHOULD**: Use `pytest.parametrize` for multiple test cases
- **SHOULD**: Use `pytest.mock` for mocking
- **SHOULD**: Use `pytest-cov` for coverage
- See Shared Patterns Agent for general testing principles
- See `.cursor/rules/practices/tdd.mdc` for TDD workflow
- Commands: `.cursor/rules/reference/commands.mdc`

### Performance
- Profile before optimizing
- Use appropriate data structures
- Consider generators for memory efficiency
- Use `__slots__` for classes with many instances

## Project Structure

See `.cursor/rules/reference/project_structure.mdc` for Python project structure template.

## Tools Integration

- **MUST**: Use Ruff for linting and formatting (configure in `.ruff.toml`)
- **MUST**: Enable strict type checking with Mypy (configure in `mypy.ini`)
- **SHOULD**: Configure pre-commit hooks for Ruff and Mypy
- See `.cursor/rules/setup/python_tools.mdc` for setup instructions
- See `.cursor/rules/reference/commands.mdc` for all commands
