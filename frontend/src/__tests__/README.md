# Frontend Tests

**Related documentation:**
- **[../../../Docs/SystemDesign.md](../../../Docs/SystemDesign.md)** - Architecture and test plan
- **[../../../Docs/TZ.md](../../../Docs/TZ.md)** - Technical requirements and acceptance criteria

## Structure

```
src/
├── __tests__/               # Integration tests
│   └── App.integration.test.tsx
└── components/
    ├── Map.test.tsx         # Map component tests
    └── FactionList.test.tsx # Faction list tests
```

```
e2e/
├── example.spec.ts          # Example e2e test
└── smoke.spec.ts            # Smoke tests for critical paths
```

## Running tests

```bash
# Unit/component tests (Vitest)
npm test                     # Run once
npm run test:watch           # Watch mode
npm run test:coverage        # With coverage

# E2E tests (Playwright)
npm run test:e2e             # Headless
npm run test:e2e:ui          # Interactive UI mode
```

## Test categories

- **Unit tests**: Test individual functions/utilities
- **Component tests**: Test React components in isolation
- **Integration tests**: Test component interactions with mocked APIs
- **E2E tests**: Test full user workflows (Playwright)

## Writing tests

- Use Testing Library for component tests (prefer user-centric queries)
- Mock API calls with `vi.fn()` for integration tests
- E2E tests should cover critical user paths (smoke tests)

Test naming convention:
- `ComponentName.test.tsx` for component tests
- `feature.spec.ts` for e2e tests
- Test descriptions should be user-centric: "user can create a faction"
