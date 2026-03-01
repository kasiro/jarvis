---
id: CARGO_DEPS_PORT
title: 'Очистка Cargo.toml от Windows зависимостей'
status: Todo
priority: Medium
order: 60
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
Проект содержит Windows-specific зависимости которые не нужны на Linux:
- `winapi` в `crates/jarvis-app/Cargo.toml`
- `winrt-notification` в workspace Cargo.toml
- Условные зависимости для Windows

## Solution
Сделать все Windows зависимости опциональными и добавить Linux аналоги.

## Implementation Details
### Файлы для изменения:

#### 1. `Cargo.toml` (workspace)
- **Строка 47:** Удалить `winrt-notification = "0.5"` или сделать опциональным

#### 2. `crates/jarvis-app/Cargo.toml`
- **Строки 27-28:** Сделать winapi опциональным
```toml
[target.'cfg(target_os = "windows")'.dependencies]
winapi = { version = "0.3", features = ["winuser"], optional = true }
```

#### 3. `crates/jarvis-core/Cargo.toml`
- **Строка 53:** Оставить winrt-notification optional
- **Строка 63:** Обновить lua feature

#### 4. Добавить Linux зависимости:
```toml
[target.'cfg(target_os = "linux")'.dependencies]
arboard = "3"  # clipboard
notify-rust = "4"  # notifications
tray-icon = "0.15"  # system tray
libappindicator-sys = "0.9"  # appindicator
```

### Тестирование:
- `cargo check` должен проходить без ошибок
- `cargo build` должен компилироваться
- Проверить что Windows зависимости не тянутся на Linux
