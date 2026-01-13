# Blades Backend

FastAPI backend for Blades in the Dark faction map application.

## Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -e ".[dev]"
```

## Development

```bash
# Run development server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Lint and format
ruff check .
ruff format .

# Type check
mypy .
```

## Quality checks

```bash
# Run all checks (from project root)
make check-backend
```
