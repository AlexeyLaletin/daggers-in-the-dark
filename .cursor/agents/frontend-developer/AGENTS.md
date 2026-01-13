# Frontend Developer Agent

**Purpose:** Frontend engineering standards and best practices for web UI development.

**When to use:** When writing or reviewing frontend code (TypeScript/JavaScript, React/Vue/Svelte, CSS, UI testing).

## Language Practices (TypeScript/JavaScript)

- **MUST**: Prefer TypeScript for new UI code unless the repo standard is JS.
- **MUST**: Avoid `any`; use `unknown` + narrowing, generics, and discriminated unions.
- **SHOULD**: Use `as const`, `satisfies`, and literal unions to keep types precise.
- **SHOULD**: Keep modules small; avoid large “utils” dumping grounds.
- **AVOID**: Complex implicit behavior (hidden global state, singleton mutable modules).

## UI Architecture

- **MUST**: Separate concerns: UI components vs business logic vs data access.
- **SHOULD**: Prefer composition over deep component inheritance patterns.
- **SHOULD**: Keep side effects at the edges (data fetching, storage, timers).
- **SHOULD**: Centralize API clients and error handling; avoid ad-hoc `fetch` scattered across components.
- **AVOID**: Over-abstracting components prematurely (YAGNI).

## Performance

- **MUST**: Avoid unnecessary re-renders (stable props, memoization where it matters).
- **SHOULD**: Load heavy code lazily (route-level code splitting is a good default).
- **SHOULD**: Optimize images (responsive sizes, modern formats) and avoid layout shift.
- **SHOULD**: Measure before optimizing; use browser DevTools + profiling.

## Accessibility (a11y)

- **MUST**: Ensure keyboard navigation works (focus order, visible focus).
- **MUST**: Use semantic HTML first; ARIA only when necessary.
- **SHOULD**: Provide accessible names for interactive elements (labels, `aria-label`).
- **SHOULD**: Respect reduced motion and color contrast requirements.

## Testing

- **MUST**: Unit test pure logic; component test user-visible behavior.
- **SHOULD**: Prefer user-centric tests (Testing Library style) over implementation details.
- **SHOULD**: Add a small set of e2e tests for critical flows (Playwright/Cypress), keep them stable.
- **MUST**: Run the same checks locally that CI runs (lint, typecheck, tests).

## Tooling and Conventions

- See `.cursor/rules/practices/frontend_best_practices.mdc` for detailed guidelines.
- See `.cursor/rules/setup/frontend_tools.mdc` for ESLint/Prettier/TS/testing setup guidance.
