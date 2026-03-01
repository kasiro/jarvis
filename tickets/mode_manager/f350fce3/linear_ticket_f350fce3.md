---
id: f350fce3
title: "Add Lua API for Mode Manager"
status: Done
priority: High
order: 20
created: 2026-02-26
updated: 2026-02-26
links:
  - url: ../linear_ticket_epic.md
    title: Parent Ticket
---

# Description

## Problem to solve
Lua команды не имеют доступа к Mode Manager. Нужно добавить Lua API.

## Solution
Добавить Lua bindings для ModesManager в модуле lua.rs.

## Implementation Details
- Обновить `crates/jarvis-core/src/lua.rs`
- Добавить `jarvis.modes` таблицу с функциями:
  - `jarvis.modes.set_mode(mode_name) -> bool`
  - `jarvis.modes.get_current_mode() -> string`
  - `jarvis.modes.get_available_modes() -> table`
- Интеграция с ModesManager из modes.rs
- Пример использования в документации Lua API
