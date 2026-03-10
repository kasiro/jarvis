---
id: i9j0k1l2
title: 'Пометить команды стоп/прекрати как wake_word_required: false'
status: Todo
priority: High
order: 30
created: '2026-03-09'
updated: '2026-03-09'
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
Критические команды (стоп, прекрати) требуют wake word что замедляет реакцию.

## Solution
Добавить `wake_word_required: false` в файлы команд стоп/прекрати.

## Implementation Details
- Файлы:
  - `resources/commands/stop/command.toml`
  - `resources/commands/terminate/command.toml`
- Добавить поле: `wake_word_required = false`
- Тестирование: проверить что команды работают без wake word
