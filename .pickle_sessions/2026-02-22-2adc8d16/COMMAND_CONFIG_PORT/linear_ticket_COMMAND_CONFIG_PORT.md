---
id: COMMAND_CONFIG_PORT
title: 'Обновление конфигурационных файлов команд'
status: Todo
priority: High
order: 50
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
Конфигурационные файлы команд (`command.yaml`, `command.toml`) ссылаются на AHK исполняемые файлы:
- `exe_path: ahk/*.exe`
- Windows-specific пути и команды

## Solution
Обновить все конфигурационные файлы для использования bash скриптов вместо AHK.

## Implementation Details
### Файлы для изменения:

#### 1. `resources/commands/windows/command.yaml`
- Строки 4, 17, 31, 45, 59, 73, 88, 103
- Заменить `exe_path: ahk/*.exe` на `exe_path: sh/*.sh`

#### 2. `resources/commands/browser/command.toml`
- Строки 4, 40, 68
- Аналогичная замена

#### 3. `resources/commands/volume/command.yaml`
- Заменить AHK на bash

#### 4. `resources/commands/steam/command.yaml`
- Заменить AHK на bash

#### 5. `resources/commands/jarvis/command.yaml`
- Заменить AHK на bash

#### 6. `resources/commands/weather/command.yaml`
- Заменить AHK на bash

### Формат bash команд:
```yaml
command_type: shell
exe_path: sh/screenshot.sh
args: []
```

### Rust код для выполнения:
`crates/jarvis-core/src/commands.rs` (строки 208-220)
- Добавить обработку `shell` command_type
- Использовать `Command::new("sh")` или `Command::new("bash")`

### Тестирование:
- Проверить что все команды находятся и выполняются
- Проверить передачу аргументов в скрипты
