---
id: parent
title: '[Epic] Команды без Wake Word'
status: Todo
priority: High
order: 0
created: '2026-03-09'
updated: '2026-03-09'
links:
  - url: ./prd.md
    title: PRD
---

# Description

## Problem to solve
Пользователь должен произносить wake word фразу перед каждой командой, что избыточно для простых команд и критических команд (стоп, прекрати).

## Solution
Добавить поле `wake_word_required` в YAML/TLV файлы команд и изменить STT модуль для проверки этого поля.

## Implementation Details
- Добавить поле `wake_word_required: bool` в структуру команды
- Изменить `commands.rs` для фильтрации команд без wake word
- Пометить существующие команды (стоп, прекрати)
- Документация

## Child Tickets
- `a1b2c3d4`: Добавить поле в структуру команды (Rust)
- `e5f6g7h8`: Изменить STT/распознавание команд
- `i9j0k1l2`: Пометить команды стоп/прекрати
- `m3n4o5p6`: Пометить часто используемые команды
- `q7r8s9t0`: Документация для разработчиков
