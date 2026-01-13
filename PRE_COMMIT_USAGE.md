# Pre-commit Usage Guide

## Overview

Pre-commit хуки автоматически запускаются перед каждым коммитом и выполняют:
1. **Форматирование**: ruff format, prettier
2. **Линтинг**: ruff check, eslint
3. **Типизация**: mypy (backend)
4. **Тесты**: pytest (backend), vitest (frontend)

## Installation

После клонирования репозитория:

```bash
# Установить pre-commit hooks
pre-commit install

# Запустить на всех файлах (первый раз)
pre-commit run --all-files
```

## Usage

### Обычный коммит (с тестами)

```bash
git add .
git commit -m "feat: add new feature"
```

Pre-commit автоматически запустит все проверки включая тесты.

### Быстрый коммит (пропустить тесты)

Если тесты занимают много времени, можно их пропустить:

```bash
# Пропустить только тесты
SKIP=backend-tests,frontend-tests git commit -m "wip: work in progress"

# Пропустить все хуки (не рекомендуется)
git commit --no-verify -m "emergency fix"
```

⚠️ **Внимание**: перед push обязательно запустите полную проверку:

```bash
make check
```

### Обновить хуки

```bash
# Обновить версии хуков
pre-commit autoupdate

# Переустановить хуки
pre-commit install --install-hooks
```

## Troubleshooting

### Хук не запускается

```bash
# Убедиться что хуки установлены
ls -la .git/hooks/pre-commit

# Переустановить
pre-commit uninstall
pre-commit install
```

### Тесты падают в pre-commit но работают локально

Убедитесь что:
1. Все зависимости установлены
2. База данных инициализирована (для backend)
3. `npm install` выполнен (для frontend)

### Отключить конкретный хук навсегда

Отредактируйте `.pre-commit-config.yaml` и удалите/закомментируйте нужный хук.

## Best Practices

1. **Коммитьте часто** с рабочими изменениями
2. **Запускайте pre-commit вручную** перед началом работы:
   ```bash
   pre-commit run --all-files
   ```
3. **Не используйте --no-verify** без крайней необходимости
4. **Проверяйте через make check** перед push
