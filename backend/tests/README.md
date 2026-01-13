# Backend Tests

## Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_main.py             # Basic app tests
├── test_api_factions.py     # Factions API tests
├── test_api_people.py       # People API tests
├── test_api_places.py       # Places API tests
├── test_api_graph.py        # Graph/wikilinks API tests
├── test_api_snapshots.py    # Snapshots/timeline API tests
├── test_api_tiles.py        # Territory tiles API tests
├── test_api_export_import.py # Export/import tests
└── unit/
    ├── test_wikilinks.py    # Wikilinks parser unit tests
    └── test_visibility_filter.py # GM/Player filter unit tests
```

## Running tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_api_factions.py

# Run specific test
pytest tests/test_api_factions.py::test_create_faction

# Run in verbose mode
pytest -v
```

## Test categories

- **Unit tests** (`tests/unit/`): Test individual functions/modules
- **API tests** (`tests/test_api_*.py`): Test API endpoints (integration tests)
- **Contract tests**: Validate request/response schemas (included in API tests)

## Writing tests

All tests should follow the System Design document (`Docs/SystemDesign.md`) and map to requirements in the TZ (`Docs/TZ.md`).

Test naming convention:
- `test_<action>_<expected_result>`
- Example: `test_create_faction_returns_201_with_id`

Fixtures are defined in `conftest.py` and automatically available in all test files.
