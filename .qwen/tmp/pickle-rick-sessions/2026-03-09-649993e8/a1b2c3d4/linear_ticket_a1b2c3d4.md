---
id: a1b2c3d4
title: 'Добавить поле wake_word_required в структуру команды (Rust)'
status: Todo
priority: High
order: 10
created: '2026-03-09'
updated: '2026-03-09'
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
Структура команды в Rust не поддерживает поле для указания необходимости wake word.

## Solution
Добавить опциональное поле `wake_word_required` в `JCommand` struct.

## Implementation Details
- Файл: `crates/jarvis-core/src/commands/structs.rs`
- Добавить поле: `#[serde(default = "default_true")] pub wake_word_required: bool`
- Default: `true` (обратная совместимость)
- Функция helper: `fn default_true() -> bool { true }`
