---
id: TAURI_CONFIG_PORT
title: 'Адаптация Tauri конфигурации и иконок'
status: Todo
priority: Low
order: 70
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
Tauri конфигурация содержит Windows-specific настройки:
- `.ico` иконки в `tauri.conf.json`
- Windows-specific paths и имена файлов

## Solution
Добавить Linux-specific иконки и настройки.

## Implementation Details
### Файл для изменения:
`crates/jarvis-gui/tauri.conf.json`

### Изменения:

#### 1. Иконки (строки 24-29)
Добавить Linux форматы:
```json
"icon": [
  "icons/icon.ico",
  "icons/icon.png",
  "icons/icon.svg"
]
```

#### 2. Имена исполняемых файлов
Проверить все упоминания `.exe` расширений

#### 3. Linux bundle settings
Добавить настройки для deb/appimage:
```json
"bundle": {
  "linux": {
    "deb": {
      "depends": ["xdotool", "wmctrl", "xclip", "libnotify"]
    }
  }
}
```

### Frontend изменения:
`crates/jarvis-gui/src/tauri_commands/sys.rs` (строка 135-136)
- Заменить `jarvis-app.exe` на `jarvis-app` для Linux

### Тестирование:
- Проверить сборку Tauri приложения
- Проверить что иконки отображаются корректно
