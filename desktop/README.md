# Blades Desktop

Electron desktop application wrapper for Blades Faction Map.

## Development

```bash
# Install dependencies
npm install

# Run in development mode (requires frontend dev server running)
npm run dev

# Build for production
npm run build

# Package application
npm run package
```

## Architecture

- **main.ts**: Electron main process, starts Python backend
- **preload.ts**: Bridge between renderer and main process
- Backend is spawned as child process on localhost:8000
- Frontend is loaded from dev server (dev) or bundled files (prod)

## Prerequisites

- Python 3.11+ with backend dependencies installed
- Node.js 18+
- Frontend built (`cd ../frontend && npm run build`)

## Production Build

```bash
# 1. Build backend (if needed)
cd ../backend
# Backend is used directly from source

# 2. Build frontend
cd ../frontend
npm run build

# 3. Package Electron app
cd ../desktop
npm run package
```

The packaged app will include:
- Electron wrapper
- Python backend (source)
- Frontend (built)

Users will need Python installed to run the app.

## Future improvements

- Bundle Python runtime with app (pyinstaller or embed Python)
- Auto-update support
- Better error handling for backend startup
- Icon and splash screen
