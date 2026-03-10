---
id: m3n4o5p6
title: 'Пометить часто используемые команды как wake_word_required: false'
status: Todo
priority: Medium
order: 40
created: '2026-03-09'
updated: '2026-03-09'
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
Часто используемые команды (браузер, погода) требуют wake word что избыточно.

## Solution
Добавить `wake_word_required: false` для часто используемых команд.

## Implementation Details
- Файлы:
  - `resources/commands/browser/command.toml`
  - `resources/commands/weather/command.toml`
  - `resources/commands/calculator/command.toml`
- Добавить поле: `wake_word_required = false`
- Тестирование: проверить работу без wake word
