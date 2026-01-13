## Devcontainer (Podman + compose)

Этот проект использует **Dev Containers** и **compose** для разработки. Контейнерный движок — **Podman** (без Docker Desktop).

### Что создаётся

- **`dev`**: рабочий контейнер для разработки (Node.js + Python + common utils)
- **`db`**: PostgreSQL 16
- **`redis`**: Redis 7

Файлы:
- `.devcontainer/devcontainer.json`
- `.devcontainer/compose.yml`
- `.devcontainer/Dockerfile`

### Требования (Podman)

Dev Containers в VS Code/ Cursor обычно ожидают **Docker CLI** (команду `docker`). В нашем случае используется **Podman**, поэтому нужно либо:

- настроить Dev Containers на использование Podman как docker CLI (рекомендовано)
- или поставить docker-алиас (`podman-docker`)

- **macOS (Podman Desktop)**:
  - установи Podman Desktop
  - запусти Podman Machine
  - включи **Docker API** (compatibility) в Podman Desktop (или настрой сокет вручную)
  - убедись, что Docker API сокет доступен (часто это `unix:///var/run/docker.sock` или путь, который покажет Podman Desktop)

- **macOS (brew podman)**:
  - Podman должен быть доступен как `/opt/homebrew/bin/podman`
  - добавь в настройки Cursor/VS Code (User или Workspace):

```json
{
  "dev.containers.dockerPath": "/opt/homebrew/bin/podman"
}
```

В этом репозитории уже добавлено workspace-настройкой: `.vscode/settings.json`.

- **Linux**:
  - установи `podman`
  - включи Docker API сервис:

```bash
sudo systemctl enable --now podman.socket
export DOCKER_HOST=unix:///run/podman/podman.sock
```

Важно: Dev Containers обычно дергают `docker compose ...`. Самый стабильный вариант — установить **Docker CLI (без Engine)** и направить его на Podman через `DOCKER_HOST`.

### Как открыть

- В Cursor/VS Code: **Dev Containers: Reopen in Container**
- Будут подняты сервисы из `.devcontainer/compose.yml`

### Подключения

- **Postgres**: `postgresql://app:app@db:5432/app`
- **Redis**: `redis://redis:6379/0`
