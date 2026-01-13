# Cursor Agent Instructions (Vendor-Neutral)

## Overview

This repository includes a set of Cursor agents and rules to keep code quality consistent across the team.

All guidance here is **vendor-neutral** (no internal tooling assumptions) and should work in any Git-based repository.

## Quick Start

1. **Select your role** - Choose appropriate role-specific instructions
2. **Review the index** - Start at `.cursor/rules/reference/INDEX.mdc`
3. **Follow best practices** - See `.cursor/rules/practices/` for documentation, TDD, and LLM filtering guidelines
4. **Set up tools** - Follow `.cursor/rules/setup/` guides for Python tools, validation, and security

## Agent Structure

This configuration uses nested `AGENTS.md` files organized by role and purpose. Each agent is defined in a separate subdirectory with its own `AGENTS.md` file. Cursor automatically applies instructions from nested `AGENTS.md` files when working with files in those directories or their subdirectories.

### Core Agents

These agents are always active and provide foundational rules:

- **[Base Agent](.cursor/agents/base/AGENTS.md)** - General engineering rules applicable to all roles
- **[Shared Patterns Agent](.cursor/agents/shared-patterns/AGENTS.md)** - Common patterns, anti-patterns, and shared principles

### Role-Specific Agents

Select the appropriate agent based on your role. These agents are automatically applied when working in their respective directories:

- **[Python Developer Agent](.cursor/agents/python-developer/AGENTS.md)** - Python-specific coding standards and best practices
- **[C++ Developer Agent](.cursor/agents/cpp-developer/AGENTS.md)** - C++-specific coding standards and best practices
- **[System Architect Agent](.cursor/agents/system-architect/AGENTS.md)** - System architecture design patterns and documentation requirements
- **[QA Engineer Agent](.cursor/agents/qa-engineer/AGENTS.md)** - QA-specific testing guidelines and quality gates

## How Nested Agents Work

According to Cursor documentation, nested `AGENTS.md` files are automatically applied when working with files in their directories:

- Instructions from nested `AGENTS.md` files are merged with parent directory instructions
- More specific instructions (from deeper directories) have priority
- This allows fine-grained control over agent instructions based on the part of codebase you're working with

## Reference Documentation

For detailed guides, see:

- **Commands**: `.cursor/rules/reference/commands.mdc` - All development commands
- **Project Structure**: `.cursor/rules/reference/project_structure.mdc` - Project templates
- **Navigation**: `.cursor/rules/reference/INDEX.mdc` - Documentation index
- **Practices**: `.cursor/rules/practices/` - Best practices (documentation, TDD, LLM filtering)
- **Setup**: `.cursor/rules/setup/` - Setup guides (Python tools, validation, security)

## Quick Reference

- **All commands**: See `.cursor/rules/reference/commands.mdc`
- **Navigation**: See `.cursor/rules/reference/INDEX.mdc`
- **Role agents**: See corresponding `AGENTS.md` files in `.cursor/agents/[role]/`
