---
id: c52612a9
title: "Create Mode Switch Commands"
status: Done
priority: High
order: 30
created: 2026-02-26
updated: 2026-02-26
links:
  - url: ../linear_ticket_epic.md
    title: Parent Ticket
---

# Description

## Problem to solve
Нет голосовых команд для переключения режимов. Существующие Python скрипты нужно заменить.

## Solution
Создать команды в resources/commands/modes/ с использованием Lua API.

## Implementation Details
- Обновить `resources/commands/modes/command.yaml`:
  - Команда "kid_mode_on" - переключение в kid mode
  - Команда "kid_mode_off" - переключение в normal mode
  - Команда "dev_mode_on" - переключение в dev mode
  - Команда "check_mode" - показать текущий режим
- Создать Lua скрипты для каждой команды
- Обновить kid_mode_on.py и kid_mode_off.py для использования Lua API
- Фразы RU: "детский режим", "обычный режим", "режим разработчика"
- Фразы EN: "kid mode", "normal mode", "developer mode"
