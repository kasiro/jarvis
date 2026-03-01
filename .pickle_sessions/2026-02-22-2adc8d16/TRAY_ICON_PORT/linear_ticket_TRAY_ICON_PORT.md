---
id: TRAY_ICON_PORT
title: 'Адаптация tray icon и Windows message pump'
status: Todo
priority: Medium
order: 40
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
Файл `crates/jarvis-app/src/tray.rs` содержит:
1. Windows-specific message pump (PeekMessageW, TranslateMessage, DispatchMessageW)
2. Windows-specific imports winit::platform::windows
3. Специфичную обработку tray icon

## Solution
Использовать GTK tray на Linux с libappindicator. Удалить Windows message pump или сделать его опциональным.

## Implementation Details
### Файл для изменения:
`crates/jarvis-app/src/tray.rs`

### Изменения:
1. **Строка 11:** Условный импорт
```rust
#[cfg(target_os = "windows")]
use winit::platform::windows::EventLoopBuilderExtWindows;
```

2. **Строки 57-74:** Windows message pump только для Windows
```rust
#[cfg(target_os = "windows")]
{
    // Message pump code
}
```

3. **Linux tray:** Использовать `tray-icon` crate с GTK
```toml
[target.'cfg(target_os = "linux")'.dependencies]
tray-icon = "0.15"
libappindicator-sys = "0.9"
```

### Tauri конфигурация:
Проверить `tauri.conf.json` на предмет tray settings
Убедиться что `tauri > systemTray` настроен правильно

### Тестирование:
- Проверить отображение иконки в GNOME tray
- Проверить контекстное меню tray
- Проверить что приложение не падает без tray
