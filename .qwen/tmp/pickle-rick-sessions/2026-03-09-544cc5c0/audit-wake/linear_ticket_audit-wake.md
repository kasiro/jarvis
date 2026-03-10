---
id: audit-wake
title: 'Code Audit: Проверка wake_word_required протокола'
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
Неизвестно какие команды нарушают протокол wake_word_required.

## Solution
Просканировать все команды и проверить наличие флага wake_word_required.

## Implementation Details
- Сканировать `resources/commands/**/*.{toml,yaml}`
- Проверить наличие `wake_word_required`
- Составить отчёт о нарушениях
- Предложить исправления
- Создать `research_audit.md`, `plan_audit.md`, `plan_review.md`
