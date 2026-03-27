# Research: Jarvis API Logger Dual Output

## Analysis Date: 2026-03-27

## Current Implementation

### File: `resources/commands/jarvis_api/core.py`

```python
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

def log(level: str, message: str) -> None:
    level = level.lower()
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    # ... etc
```

### Problem Analysis

**ISSUE #1: No Handlers Configured**
- `logging.getLogger(__name__)` создаёт logger БЕЗ handlers
- Python's logging module по умолчанию имеет root logger с warning level
- Log сообщения уровня `debug` и `info` НЕ ВЫВОДЯТСЯ

**ISSUE #2: No File Output**
- Даже если бы handlers были, нет FileHandler для записи в файл
- Только `print(..., file=sys.stderr)` работает для вывода в консоль

**ISSUE #3: Dependency on jarvis_server.py**
- `jarvis_server.py` имеет `logging.basicConfig()` с StreamHandler
- Но это настраивает только root logger, не `jarvis_api.core` logger

## Solution Design

### Approach: Lazy Initialization with Dual Handlers

```python
import logging
import os
from pathlib import Path

_logger_initialized = False

def _setup_logger(log_file_path: str = None) -> None:
    """
    Инициализировать logger с dual output (console + file)
    """
    global _logger_initialized
    
    if _logger_initialized:
        return
    
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Полный уровень для logger
    logger.propagate = False  # Предотвратить дублирование в root logger
    
    # Очистить существующие handlers
    logger.handlers.clear()
    
    # 1. StreamHandler для console (stderr)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter(
        '[Jarvis:%(levelname)s] %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 2. FileHandler для file (опционально)
    if log_file_path:
        try:
            # Создать директорию если не существует
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s [Jarvis:%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # Fallback: только console если файл недоступен
            logger.warning(f"Failed to setup file logging: {e}")
    
    _logger_initialized = True
```

### Integration Strategy

**Option A: Pass log_path from context**
- Rust core передаёт `log_file_path` в Python context
- `init_jarvis(context)` вызывает `_setup_logger(context.get('log_file'))`

**Option B: Use default path**
- Использовать стандартный путь: `~/.local/share/jarvis/logs/jarvis_api.log`
- Не требует изменений в Rust

**RECOMMENDED: Option B + Override**
- Использовать default path по умолчанию
- Позволить override через context если предоставлен

## Implementation Plan

1. **Modify `core.py`:**
   - Добавить `_setup_logger()` функцию
   - Добавить `_logger_initialized` flag
   - Вызывать `_setup_logger()` в начале `log()` функции
   - Использовать default log path или из environment variable

2. **Testing:**
   - Создать тестовый скрипт для проверки dual output
   - Проверить все уровни логирования
   - Проверить обработку ошибок файла

## Files to Modify

- `resources/commands/jarvis_api/core.py` - Основная реализация

## Files to Create (Optional)

- `resources/commands/jarvis_api/logging_config.py` - Выделенный модуль (если нужно)

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Directory не существует | `os.makedirs(exist_ok=True)` |
| Нет прав на запись | Try/except, fallback к console-only |
| Дублирование логов | `logger.propagate = False` |
| Performance impact | Buffered FileHandler, async write (optional) |

## Conclusion

Реализация dual output logging требует:
1. Добавления `_setup_logger()` с lazy initialization
2. Добавления StreamHandler + FileHandler
3. Обработки ошибок для file operations
4. Использования default log path с возможностью override
