---
id: e5a044b4
title: "Implement Rust ModesManager Module"
status: Done
priority: High
order: 10
created: 2026-02-26
updated: 2026-02-26
links:
  - url: ../linear_ticket_epic.md
    title: Parent Ticket
---

# Description

## Problem to solve
Python ModesManager существует но не интегрирован в Rust ядро. Нужно создать Rust реализацию.

## Solution
Создать новый модуль `modes.rs` в jarvis-core с ModesManager struct для управления режимами.

## Implementation Details
- Создать `crates/jarvis-core/src/modes.rs`
- Реализовать `ModesManager` struct с методами:
  - `new()` - инициализация с загрузкой из state.db
  - `set_mode(&mut self, mode: &str) -> Result<bool>` - переключение режима
  - `get_current_mode(&self) -> &str` - получение текущего режима
  - `get_available_modes(&self) -> Vec<&str>` - список режимов
- MODES = ["normal", "kid", "dev"]
- Интеграция с state.db для сохранения состояния
- Публикация событий в event bus при смене режима
