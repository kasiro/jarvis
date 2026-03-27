# Implementation Plan: Dual Output Logger

## Ticket: impl_jarvis_api_logger_dual

## Phase: Implementation

## Objective

Модифицировать `jarvis_api/core.py` для поддержки одновременной записи логов в консоль (stderr) и файл.

## Implementation Steps

### Step 1: Modify `core.py`

**File:** `resources/commands/jarvis_api/core.py`

**Changes:**

1. Добавить импорты:
   ```python
   import os
   from pathlib import Path
   from typing import Optional
   ```

2. Добавить глобальные переменные:
   ```python
   _logger_initialized = False
   _default_log_path = None
   ```

3. Добавить функцию `_setup_logger()`:
   ```python
   def _setup_logger(log_file_path: Optional[str] = None) -> None:
       """
       Инициализировать logger с dual output (console + file)
       
       Args:
           log_file_path: Путь к файлу логов (опционально)
       """
       global _logger_initialized
       
       if _logger_initialized:
           return
       
       logger.setLevel(logging.DEBUG)
       logger.propagate = False
       logger.handlers.clear()
       
       # StreamHandler для console
       console_handler = logging.StreamHandler(sys.stderr)
       console_handler.setLevel(logging.DEBUG)
       console_formatter = logging.Formatter('[Jarvis:%(levelname)s] %(message)s')
       console_handler.setFormatter(console_formatter)
       logger.addHandler(console_handler)
       
       # FileHandler для file
       if log_file_path:
           try:
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
               logger.warning(f"Failed to setup file logging: {e}")
       
       _logger_initialized = True
   ```

4. Модифицировать функцию `log()`:
   ```python
   def log(level: str, message: str) -> None:
       # Инициализировать logger при первом вызове
       if not _logger_initialized:
           # Получить путь из environment или использовать default
           log_path = os.environ.get('JARVIS_LOG_FILE')
           if not log_path:
               # Default путь: ~/.local/share/jarvis/logs/jarvis_api.log
               home = Path.home()
               log_dir = home / '.local' / 'share' / 'jarvis' / 'logs'
               log_path = str(log_dir / 'jarvis_api.log')
           _setup_logger(log_path)
       
       # Остальной код...
   ```

### Step 2: Testing

**Create test script:** `test_logger.py`

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'resources/commands')

from jarvis_api.core import log

# Test all levels
log("debug", "Debug message")
log("info", "Info message")
log("warn", "Warning message")
log("error", "Error message")

print("Logger test completed!")
```

**Run test:**
```bash
cd /home/kasiro/Документы/jarvis
python3 test_logger.py
```

**Verify:**
1. Messages appear in stderr
2. Messages written to `~/.local/share/jarvis/logs/jarvis_api.log`
3. File contains timestamps
4. All log levels work correctly

### Step 3: Cleanup

- Remove test script
- Verify no temporary files left

## Success Criteria

- [ ] `jarvis.log()` пишет в stderr
- [ ] `jarvis.log()` пишет в файл
- [ ] Файл создаётся в `~/.local/share/jarvis/logs/`
- [ ] Timestamps в файле
- [ ] Все уровни работают (debug, info, warn, error)
- [ ] Ошибки файла не ломают выполнение

## Rollback Plan

Если что-то пойдёт не так:
```bash
git checkout resources/commands/jarvis_api/core.py
```

## Files to Modify

| File | Change Type |
|------|-------------|
| `resources/commands/jarvis_api/core.py` | Modify |

## Files to Create (Temporary)

| File | Purpose |
|------|---------|
| `test_logger.py` | Testing |

## Estimated Time

15-30 minutes
