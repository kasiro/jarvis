---
id: test-commands
title: 'Testing: Тестирование команд без wake word'
status: Todo
priority: High
order: 20
created: '2026-03-09'
updated: '2026-03-09'
links:
  - url: ../parent/linear_ticket_parent.md
    title: Parent Ticket
---

# Description

## Problem to solve
Требуется проверить что команды с wake_word_required: false работают без wake word.

## Solution
Протестировать каждую команду с флагом и проверить что voice команды требуют wake word.

## Implementation Details
- Запустить Jarvis в тестовом режиме
- Протестировать команды с wake_word_required: false
- Проверить что voice команды НЕ работают без wake word
- Составить отчёт о результатах
- Создать `research_testing.md`, `plan_testing.md`, `plan_review.md`
