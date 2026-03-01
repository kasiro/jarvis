---
id: SYSTEM_API_PORT
title: 'Адаптация системных API: clipboard, notifications, exec'
status: Todo
priority: High
order: 20
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
Файл `crates/jarvis-core/src/lua/api/system.rs` использует Windows-specific API:
- PowerShell для clipboard (Get-Clipboard, Set-Clipboard)
- cmd.exe для выполнения команд
- WinRT для уведомлений
- msg.exe для fallback уведомлений

## Solution
Добавить Linux-реализации с использованием:
- xclip/wl-clipboard для буфера обмена
- sh/bash для выполнения команд
- notify-send/dbus для уведомлений

## Implementation Details
### Файл для изменения:
`crates/jarvis-core/src/lua/api/system.rs`

### Изменения по функциям:

#### 1. `jarvis.system.open()` (строка 13)
**Windows:** `cmd /C start "" target`
**Linux:** `xdg-open target`

#### 2. `jarvis.system.exec()` (строка 40)
**Windows:** `cmd /C cmd`
**Linux:** `sh -c cmd`

#### 3. `jarvis.system.notify()` (строка 78)
**Windows:** WinRT Toast + msg.exe fallback
**Linux:** `notify-send` через Command или dbus crate

#### 4. `jarvis.clipboard.get()` (строка 124)
**Windows:** `powershell Get-Clipboard`
**Linux:** `xclip -o` или `wl-paste` (для Wayland)

#### 5. `jarvis.clipboard.set()` (строка 168)
**Windows:** `powershell Set-Clipboard`
**Linux:** `xclip -selection clipboard` или `wl-copy`

#### 6. Определение платформы (строка 226)
Добавить Linux-specific пути и имена процессов

### Зависимости для добавления:
```toml
[target.'cfg(target_os = "linux")'.dependencies]
arboard = "3"  # Кроссплатформенный clipboard
notify-rust = "4"  # Уведомления через dbus
```

### Тестирование:
- Проверить работу на GNOME Wayland
- Убедиться что xclip/wl-clipboard установлены или добавить проверку
