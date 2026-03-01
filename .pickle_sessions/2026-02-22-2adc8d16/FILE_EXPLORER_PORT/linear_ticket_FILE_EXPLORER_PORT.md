---
id: FILE_EXPLORER_PORT
title: 'Адаптация file explorer: Nautilus вместо explorer.exe'
status: Todo
priority: Medium
order: 30
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
Файл `crates/jarvis-gui/src/tauri_commands/fs.rs` использует `explorer.exe` для показа файлов в проводнике Windows.

## Solution
Заменить на `xdg-open` или `nautilus` для GNOME.

## Implementation Details
### Файл для изменения:
`crates/jarvis-gui/src/tauri_commands/fs.rs` (строка 11-17)

### Текущий код:
```rust
#[cfg(target_os = "windows")]
Command::new("explorer")
    .args(["/select,", &path])
    .spawn()
```

### Linux реализация:
```rust
#[cfg(target_os = "linux")]
Command::new("xdg-open")
    .arg(parent_path)
    .spawn()
// или для Nautilus:
Command::new("nautilus")
    .arg(parent_path)
    .spawn()
```

### Frontend изменения:
`frontend/src/functions.ts` - функция `showInExplorer()` должна работать корректно

### Тестирование:
- Проверить открытие папки с файлом
- Проверить выделение файла (если возможно на Linux)
