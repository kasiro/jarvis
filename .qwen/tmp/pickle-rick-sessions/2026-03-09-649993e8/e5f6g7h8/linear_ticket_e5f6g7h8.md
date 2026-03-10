---
id: e5f6g7h8
title: 'Изменить STT/распознавание для проверки wake_word_required'
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
STT модуль не проверяет поле `wake_word_required` перед выполнением команды.

## Solution
Изменить логику выполнения команд в `commands.rs` для проверки поля.

## Implementation Details
- Файл: `crates/jarvis-core/src/commands.rs`
- Перед выполнением команды проверить: `if !cmd.wake_word_required { execute immediately }`
- Интеграция с STT потоком
- Приоритет команд без wake word
