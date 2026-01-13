# C++ Developer Agent

**Purpose:** C++-specific coding standards and best practices.

**When to use:** When writing C++ code in this repository.

## Code Style

### Naming Conventions
- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `kConstantName` or `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore` or `trailing_underscore_`
- Namespaces: `snake_case`
- Macros: `UPPER_SNAKE_CASE`

### Header Files
- Use header guards: `#ifndef PROJECT_MODULE_H_` / `#define PROJECT_MODULE_H_`
- Or use `#pragma once` (if supported)
- Include what you use
- Forward declare when possible
- Organize includes: system headers, third-party, local

### Code Organization
```cpp
// Good header structure
#ifndef PROJECT_MODULE_H_
#define PROJECT_MODULE_H_

#include <vector>
#include <string>

namespace project {
namespace module {

class MyClass {
public:
    MyClass();
    ~MyClass();

    void PublicMethod(int arg);

private:
    int member_variable_;
    void PrivateMethod();
};

}  // namespace module
}  // namespace project

#endif  // PROJECT_MODULE_H_
```

## C++ Best Practices

### Memory Management
- Use smart pointers (`std::unique_ptr`, `std::shared_ptr`) instead of raw pointers
- Prefer stack allocation over heap when possible
- Use RAII for resource management
- Avoid memory leaks - always pair new/delete, malloc/free
- Use containers (`std::vector`, `std::string`) instead of C arrays

### Modern C++ Features
- Use `auto` when type is obvious
- Use range-based for loops
- Use `nullptr` instead of `NULL`
- Use `constexpr` for compile-time constants
- Use `override` for virtual function overrides
- Prefer `enum class` over plain `enum`

### Error Handling
- **MUST**: Use exceptions for error handling (not error codes)
- **SHOULD**: Use `noexcept` when function cannot throw
- **SHOULD**: Document exception guarantees
- **MUST**: Use RAII to ensure cleanup on exceptions
- See Shared Patterns Agent for general error handling principles

### Performance
- Avoid premature optimization
- Profile before optimizing
- Use `const` and `constexpr` appropriately
- Use move semantics when appropriate
- Avoid unnecessary copies

## Build System Integration

- Follow this repository’s build system (commonly CMake, Bazel, Meson, etc.).
- Keep build definitions minimal and readable.
- Add tests to the build in a way that works in CI (avoid machine-local paths).

## Project Structure

See `.cursor/rules/reference/project_structure.mdc` for C++ project structure template.

## Testing
- **MUST**: Write unit tests for all public APIs
- **MUST**: Test edge cases and error conditions
- **SHOULD**: Use test fixtures for setup/teardown
- **SHOULD**: Mock external dependencies
- **SHOULD**: Use test data generators
- **MUST**: Run tests using the repo’s standard command (e.g. `ctest`, `ninja test`, or the CI-equivalent)
- See Shared Patterns Agent for general testing principles
