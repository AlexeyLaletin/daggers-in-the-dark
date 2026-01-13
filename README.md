# Blades in the Dark: Faction Map

Interactive web application for Game Masters to visualize and manage faction territories, characters, places, and their relationships in Blades in the Dark RPG campaigns.

## Features

### Core Functionality (MVP Complete ✅)
- ✅ **Faction Management**: Create, edit factions with colors and opacity
- ✅ **Territory Tiles API**: Backend support for storing territory masks (Canvas painting UI - future iteration)
- ✅ **Entity Management**: People, Places, Factions with rich notes (public/GM-only)
- ✅ **Wikilinks & Graph**: Obsidian-style `[[wikilinks]]` in markdown with automatic link resolution and backlinks
- ✅ **GM/Player Modes**: Toggle between full GM view and filtered Player view
- ✅ **Timeline/Snapshots**: Save and switch between different city states by date
- ✅ **Export/Import**: Transfer projects between devices via SQLite file

### Architecture
- **Backend**: Python + FastAPI + SQLite (thin client architecture)
- **Frontend**: React + TypeScript + Vite
- **Desktop**: Electron wrapper (spawns local backend, loads frontend)
- **Quality**: Ruff, Mypy, ESLint, Prettier, pytest, Vitest, pre-commit hooks

## Project Structure

```
daggers-in-the-dark/
├── backend/          # FastAPI backend (Python)
│   ├── app/
│   │   ├── api/      # REST endpoints
│   │   ├── models.py # SQLModel models
│   │   ├── schemas.py # Pydantic schemas
│   │   └── services/ # Business logic (wikilinks, graph)
│   ├── tests/        # pytest tests
│   └── pyproject.toml
├── frontend/         # React frontend (TypeScript)
│   ├── src/
│   │   ├── api/      # API client
│   │   ├── components/ # React components
│   │   └── contexts/  # Context providers (ViewMode)
│   ├── e2e/          # Playwright e2e tests
│   └── package.json
├── desktop/          # Electron wrapper
│   └── src/
│       ├── main.ts   # Main process (spawns backend)
│       └── preload.ts # IPC bridge
├── Docs/
│   ├── TZ.md         # Technical Specification (Russian)
│   └── SystemDesign.md # Detailed system design
└── Makefile          # Common commands
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- uv (Python package manager)

### Development Setup

1. **Clone and setup:**
   ```bash
   git clone https://github.com/AlexeyLaletin/daggers-in-the-dark.git
   cd daggers-in-the-dark
   make install
   ```

2. **Start backend:**
   ```bash
   cd backend
   uv venv && source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   uv pip install -e ".[dev]"
   uvicorn app.main:app --reload
   ```

3. **Start frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access app:** Open http://localhost:5173

### Desktop App

```bash
# Build frontend first
cd frontend && npm run build

# Run desktop app
cd ../desktop
npm install
npm run dev
```

## Development Workflow

### Quality Checks

```bash
# Run all checks (format, lint, typecheck, tests)
make check

# Backend only
make check-backend

# Frontend only
make check-frontend
```

### Pre-commit Hooks

Pre-commit hooks are configured to run all quality checks:
```bash
# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files

# Skip tests for quick commits
SKIP=backend-tests,frontend-tests git commit
```

### Shrimp Task Manager (Cursor MCP)

This repo includes a project-level Cursor MCP config for **Shrimp Task Manager** in `.cursor/mcp.json` and an always-applied rule in `.cursor/rules/practices/shrimp_task_manager.mdc`.

## Documentation

### Project Documentation
- **[Docs/TZ.md](Docs/TZ.md)** - Technical Specification (requirements, use cases, acceptance criteria)
- **[Docs/SystemDesign.md](Docs/SystemDesign.md)** - System Design (architecture, API contracts, data models)

### Development Guides
- **[backend/README.md](backend/README.md)** - Backend setup and development
- **[frontend/README.md](frontend/README.md)** - Frontend setup and development
- **[desktop/README.md](desktop/README.md)** - Desktop (Electron) setup and development
- **[backend/tests/README.md](backend/tests/README.md)** - Backend testing guide
- **[frontend/src/__tests__/README.md](frontend/src/__tests__/README.md)** - Frontend testing guide

### Cursor AI Agent Configuration
- **[AGENTS.md](AGENTS.md)** - Cursor Agent instructions (vendor-neutral)
- **[.cursor/rules/reference/INDEX.mdc](.cursor/rules/reference/INDEX.mdc)** - Documentation index for AI agents

## API Endpoints

Backend exposes REST API at `http://localhost:8000/api`:

- `/factions` - CRUD for factions
- `/people` - CRUD for characters
- `/places` - CRUD for places
- `/pages` - CRUD for note pages (wikilinks)
- `/graph` - Graph API (nodes, edges, backlinks)
- `/snapshots` - Timeline snapshots
- `/snapshots/{id}/territory/tiles` - Territory tile storage
- `/export` - Export project as SQLite file
- `/import` - Import project from file

See [Docs/SystemDesign.md](Docs/SystemDesign.md) for detailed API contracts.

## Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test

# E2E tests
cd frontend && npm run test:e2e
```

## Contributing

1. All changes must follow [Docs/TZ.md](Docs/TZ.md)
2. Run `make check` before committing
3. Each commit must pass all quality checks and tests
4. Update TZ.md if requirements change

## Implementation Status

**MVP Complete** ✅ - All core backend/frontend infrastructure implemented:

- ✅ Environment initialization (uv, ruff, mypy, pre-commit, ESLint, Prettier, tests)
- ✅ System Design document
- ✅ Test framework (pytest, vitest, playwright)
- ✅ Backend CRUD APIs (factions, people, places, pages)
- ✅ Wikilinks parser and Graph API
- ✅ Snapshots API (timeline)
- ✅ Territory Tiles API (storage layer)
- ✅ Frontend UI with API integration
- ✅ GM/Player mode toggle
- ✅ Electron desktop wrapper
- ✅ Export/Import functionality

**Next Iterations:**
- Full Canvas implementation with actual territory painting UI
- Extended entity editors (forms for people/places with all fields)
- Advanced graph visualization component
- Timeline diff view and comparison
- Performance optimizations for large maps

## License

MIT
