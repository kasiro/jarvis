---
id: parent_jarvis_api_logger
title: '[Epic] Jarvis API Python Logger Dual Output'
status: Backlog
priority: High
order: 0
created: '2026-03-27'
updated: '2026-03-27'
links:
  - url: prd_jarvis_api_logger.md
    title: PRD Document
---

# Description

## Problem to solve
Python logger в `jarvis_api` не пишет логи в файл, только в stderr. Нужно добавить одновременную запись в консоль и файл.

## Solution
Добавить FileHandler к существующему StreamHandler в модуле `jarvis_api/core.py`.

## Implementation Details
- Модифицировать `core.py` для добавления FileHandler
- Использовать лог-директорию из контекста или default путь
- Обеспечить обработку ошибок (если директория недоступна)
- Протестировать на существующих командах
