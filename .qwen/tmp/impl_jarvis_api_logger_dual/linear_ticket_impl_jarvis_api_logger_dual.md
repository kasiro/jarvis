---
id: impl_jarvis_api_logger_dual
title: 'Implement Dual Output Logger in jarvis_api/core.py'
status: Todo
priority: High
order: 10
created: '2026-03-27'
updated: '2026-03-27'
links:
  - url: linear_ticket_parent_jarvis_api_logger.md
    title: Parent Ticket
---

# Description

## Problem to solve
Функция `log()` в `jarvis_api/core.py` использует `logging.getLogger(__name__)` без настроенных handlers. Логи не записываются в файл.

## Solution
Добавить инициализацию logging с двумя handlers:
1. StreamHandler для вывода в stderr (консоль)
2. FileHandler для записи в файл

## Implementation Details
- Создать функцию `_setup_logger()` для инициализации handlers
- Добавить параметр `log_file_path` (опционально из контекста)
- Использовать default путь если не указан
- Добавить обработку ошибок при создании файла
- Установить `propagate=False` для предотвращения дублирования
- Сохранить существующий формат сообщений

## Acceptance Criteria
- [ ] `jarvis.log("info", "test")` пишет в stderr
- [ ] `jarvis.log("info", "test")` пишет в файл
- [ ] Ошибки при записи в файл не ломают выполнение
- [ ] Все уровни логирования работают (debug, info, warn, error)
