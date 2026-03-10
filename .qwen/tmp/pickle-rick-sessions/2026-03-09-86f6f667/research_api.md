# Jarvis API Research

**Дата**: 2026-03-09  
**Исследователь**: Code Researcher  
**Цель**: Полное изучение архитектуры Jarvis API для создания новых функций

---

## 1. Executive Summary

Jarvis API представляет собой **Python-модуль** (`jarvis_api/`), предоставляющий унифицированный интерфейс для взаимодействия с различными подсистемами Jarvis:

- **Core API**: Базовые функции (log, print, sleep, speak)
- **State API**: Хранение состояния команд в `.state.json`
- **System API**: Взаимодействие с ОС (notify, open, exec, clipboard)
- **Audio API**: Воспроизведение звуков
- **HTTP API**: Асинхронные HTTP запросы (aiohttp)
- **Context API**: Доступ к контексту команды (phrase, language, slots)
- **Modes API**: Управление режимами (normal, kid, dev)
- **Environment API**: Управление окружением Wayland и окнами

**Архитектура**: Rust (jarvis-app) → Python (jarvis_server.py) → jarvis_api модули → Системные вызовы

---

## 2. Структура API

### 2.1. Список модулей

| Модуль | Файл | Описание |
|--------|------|----------|
| **Core** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/core.py` | Базовые функции: log, print_fn, sleep, speak |
| **State** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/state.py` | Хранение состояния в `.state.json` |
| **System** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/system.py` | ОС функции: notify, open, exec, clipboard, env |
| **Audio** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/audio.py` | Воспроизведение звуков (.mp3, .wav, .ogg) |
| **HTTP** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/http.py` | Async HTTP: get, post, request |
| **Context** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/context.py` | Контекст: phrase, language, slots |
| **Modes** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/modes.py` | Режимы: get_current, set_mode |
| **Environment** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/environment.py` | Wayland, окна, рабочие столы |
| **EventBus** | `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/event_bus.py` | Шина событий (async pub/sub) |

### 2.2. Паттерн создания новых API функций

**Структура нового API модуля:**

```python
"""
Module Name - Описание
"""
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class ModuleName:
    """
    ModuleName API для ...
    """

    def __init__(self):
        self._internal_state = None

    def _init_dependency(self):
        """Ленивая инициализация зависимости"""
        if self._internal_state is None:
            try:
                from dependency import DependencyClass
                self._internal_state = DependencyClass()
            except ImportError as e:
                print(f"[Jarvis:MODULE] Failed to import: {e}", file=sys.stderr)
                return None
        return self._internal_state

    def new_function(self, arg1: str, arg2: int = 0) -> bool:
        """
        Описание функции

        Args:
            arg1: Описание
            arg2: Описание

        Returns:
            True если успешно
        """
        dep = self._init_dependency()
        if not dep:
            return False

        try:
            # Логика функции
            return True
        except Exception as e:
            print(f"[Jarvis:MODULE] Error: {e}", file=sys.stderr)
            return False


# Глобальный экземпляр
module = ModuleName()
```

**Экспорт в `__init__.py`:**

```python
from .module import ModuleName, module

__all__ = [
    "ModuleName",
    "module",
]
```

**Использование в командах:**

```python
from jarvis_api import init_jarvis

async def execute(context):
    jarvis = init_jarvis(context)
    
    # Использование API
    jarvis.log("info", "Message")
    jarvis.state.set("key", "value")
    jarvis.system.notify("Title", "Text")
    jarvis.environment.press_super_number(1)
    
    return {"success": True}
```

---

## 3. Environment API

### 3.1. Существующие функции

**Wayland Control (клавиатура):**

| Функция | Описание | Параметры |
|---------|----------|-----------|
| `press_enter()` | Нажать Enter | - |
| `press_tab(count)` | Нажать Tab | `count`: количество раз |
| `press_number(number)` | Нажать цифру | `number`: 0-4 |
| `press_space()` | Нажать Space | - |
| `press_super_number(number)` | Super + цифра | `number`: 0-4 |

**Window Management:**

| Функция | Описание | Параметры |
|---------|----------|-----------|
| `get_windows()` | Список всех окон | - |
| `minimize_all_windows()` | Свернуть все окна | - |
| `maximize_all_windows()` | Развернуть все окна | - |
| `maximize_window(wm_class)` | Развернуть окно | `wm_class`: класс окна |
| `focus_window(wm_class)` | Фокус на окно | `wm_class`: класс окна |
| `is_app_running(wm_class)` | Проверка запуска | `wm_class`: класс приложения |
| `move_window_to_workspace(id, ws)` | Переместить окно | `window_id`, `workspace` (0-based) |

**Application Launching:**

| Функция | Описание | Параметры |
|---------|----------|-----------|
| `launch_app(app_name, workspace)` | Запустить приложение | `app_name`, `workspace` (1-based) |
| `launch_or_move_app(app, wm_class, ws)` | Запустить или переключиться | `app_name`, `wm_class`, `workspace` |

**Workspace Control:**

| Функция | Описание | Параметры |
|---------|----------|-----------|
| `switch_to_workspace(number)` | Переключить рабочий стол | `number`: 1-4 |

### 3.2. Что есть для работы с окнами

**Файлы:**
- `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/environment.py` - API модуль
- `/home/kasiro/Документы/jarvis/resources/commands/wayland.py` - WaylandController (pydotool)
- `/home/kasiro/Документы/jarvis/resources/commands/wm_manager.py` - WindowManager, AppLauncher, AppManager

**Зависимости:**
- **pydotool** - эмуляция ввода Wayland (ydotool)
- **gdbus** - D-Bus интерфейс для управления окнами GNOME
- **window-calls@domandoman.xyz** - GNOME extension для D-Bus

**Технические детали:**

```python
# wayland.py использует pydotool
from pydotool import (
    KEY_0, KEY_1, KEY_2, KEY_3, KEY_4,
    KEY_LEFTMETA, KEY_TAB, KEY_ENTER, KEY_SPACE
)

# wm_manager.py использует D-Bus
gdbus call --session --dest org.gnome.Shell \
  --object-path /org/gnome/Shell/Extensions/Windows \
  --method org.gnome.Shell.Extensions.Windows.List
```

### 3.3. Функции для рабочих столов

**Уже реализовано:**

```python
# Environment API
jarvis.environment.switch_to_workspace(number: int) -> bool
jarvis.environment.move_window_to_workspace(window_id: int, workspace: int) -> bool
jarvis.environment.press_super_number(number: int) -> bool  # Super+1, Super+2, etc.

# WindowManager
wm.move_to_workspace(window_id: int, workspace: int) -> bool

# AppLauncher
launcher.launch(app_name: str, workspace: int) -> str
launcher.launch_or_move(appname: str, wm_class: str, workspace: int)
```

**НО**: Нет отдельных API функций для:
- Получения текущего рабочего стола
- Переключения на следующий/предыдущий рабочий стол
- Перемещения текущего окна на другой рабочий стол
- Получения списка всех рабочих столов

---

## 4. Архитектура

### 4.1. Как создавать новые функции

**Шаг 1: Создать API функцию в модуле**

```python
# jarvis_api/environment.py
def get_current_workspace(self) -> int:
    """
    Получить текущий рабочий стол

    Returns:
        Номер рабочего стола (1-based)
    """
    wayland = self._init_wayland()
    if not wayland:
        return 1  # Default

    try:
        # Логика получения текущего рабочего стола
        # Например, через D-Bus
        wm = self._init_window_manager()
        # ... реализация
        return current_workspace
    except Exception as e:
        print(f"[Jarvis:ENV] Error getting workspace: {e}", file=sys.stderr)
        return 1
```

**Шаг 2: Добавить экспорт в `__init__.py`**

```python
# jarvis_api/__init__.py
# Функция автоматически экспортируется через класс Environment
```

**Шаг 3: Использовать в команде**

```python
from jarvis_api import init_jarvis

async def execute(context):
    jarvis = init_jarvis(context)
    
    current_ws = jarvis.environment.get_current_workspace()
    jarvis.log("info", f"Current workspace: {current_ws}")
    
    return {"success": True}
```

### 4.2. Интеграция

**Rust → Python:**

```rust
// crates/jarvis-core/src/commands.rs
#[cfg(feature = "python")]
fn execute_python(...) {
    // Spawn Python server via uv run
    let mut child = Command::new("uv")
        .args(["run", "--with", "aiohttp", "python", "-m", "jarvis_server"])
        .current_dir(&APP_DIR)
        .env("PYTHONPATH", APP_DIR.join("resources/commands"))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()?;

    // Send context via stdin (JSON)
    let context = json!({
        "phrase": phrase.unwrap_or(""),
        "language": i18n::get_language(),
        "slots": slots,
        "command_path": cmd_path,
        "module": module_path,
    });
    
    child.stdin.write_all(context.to_string().as_bytes())?;
}
```

**Python Server → API:**

```python
# jarvis_server.py
async def handle_request(request: dict):
    module = importlib.import_module(module_name)
    
    # Инициализируем jarvis с контекстом
    from jarvis_api import init_jarvis
    jarvis = init_jarvis(context)
    
    # Выполняем команду
    result = await module.execute(context)
    
    return {"success": True, "result": result}
```

**Контекст передаётся:**
1. Rust создаёт JSON контекст
2. Отправляет в stdin Python процесса
3. `jarvis_server.py` парсит JSON
4. `init_jarvis(context)` инициализирует все API модули
5. Команда использует `jarvis.*` API

---

## 5. Зависимости

### 5.1. Что используется

**Python зависимости** (`pyproject.toml`):

```toml
dependencies = [
    "aiohttp>=3.13.3",      # Async HTTP
    "pyautogui>=0.9.54",    # GUI automation (не используется напрямую)
    "python-ydotool>=1.1.0", # Wayland input emulation (pydotool)
]
```

**Системные зависимости:**

| Компонент | Зависимость | Назначение |
|-----------|-------------|------------|
| **Wayland** | `ydotool`, `pydotool` | Эмуляция ввода |
| **Window Manager** | `gdbus`, GNOME extension | Управление окнами |
| **Audio** | `paplay`, `aplay`, `ffplay` | Воспроизведение звуков |
| **Notifications** | `notify-send` (Linux) | Системные уведомления |
| **Clipboard** | `xclip`, `xsel` (Linux) | Буфер обмена |

### 5.2. Что нужно добавить

**Для расширения Environment API:**

1. **D-Bus функции для рабочих столов:**
   ```bash
   # Получить текущий рабочий стол
   gdbus call --session --dest org.gnome.Shell \
     --object-path /org/gnome/Shell/Extensions/Windows \
     --method org.gnome.Shell.Extensions.Windows.GetCurrentWorkspace
   
   # Получить список рабочих столов
   gdbus call --session --dest org.gnome.Shell \
     --object-path /org/gnome/Shell/Extensions/Windows \
     --method org.gnome.Shell.Extensions.Windows.ListWorkspaces
   ```

2. **Python зависимости (опционально):**
   - `dbus-python` или `jeepney` - для прямого D-Bus доступа
   - `pygobject` - для GNOME API

3. **Новые API функции (рекомендации):**
   ```python
   # Environment API
   jarvis.environment.get_current_workspace() -> int
   jarvis.environment.get_workspace_count() -> int
   jarvis.environment.next_workspace() -> bool
   jarvis.environment.previous_workspace() -> bool
   jarvis.environment.move_current_window_to_workspace(workspace: int) -> bool
   jarvis.environment.get_windows_on_workspace(workspace: int) -> List[Dict]
   ```

---

## 6. Примеры использования

### 6.1. Существующие команды

**Kid Mode ON** (`/home/kasiro/Документы/jarvis/resources/commands/modes/kid_mode_on.py`):

```python
from jarvis_api import init_jarvis

async def execute(context):
    jarvis = init_jarvis(context)
    
    # Переключение режима
    success = await jarvis.modes.set_mode("kid")
    
    # Управление окнами
    jarvis.environment.minimize_all_windows()
    
    # Запуск приложения
    jarvis.system.exec_background("mullvad-browser --new-window https://www.youtubekids.com")
    
    # Эмуляция клавиатуры
    jarvis.environment.press_tab(2)
    jarvis.environment.press_enter()
    
    return {"success": True}
```

**Browser Open** (`/home/kasiro/Документы/jarvis/resources/commands/browser/sh/open_browser.py`):

```python
from jarvis_api import init_jarvis

async def execute(context):
    jarvis = init_jarvis(context)
    
    # Запуск или переключение на браузер
    jarvis.environment.launch_or_move_app("firefox", "firefox", 1)
    
    return {"success": True}
```

### 6.2. Шаблон новой команды

```python
#!/usr/bin/env python3
"""
Command Name - Описание

Команды:
- "фраза 1"
- "фраза 2"
"""

from jarvis_api import init_jarvis


async def execute(context):
    """
    Выполнить команду

    Args:
        context: Контекст команды
    """
    jarvis = init_jarvis(context)
    jarvis.log("info", "Executing command...")

    # Использование API
    jarvis.audio.play_ok()
    jarvis.state.set("key", "value")
    jarvis.system.notify("Title", "Message")
    
    # Environment API
    jarvis.environment.press_super_number(1)
    jarvis.environment.switch_to_workspace(2)
    
    return {"success": True}
```

---

## 7. Тесты

**Файлы тестов:**
- `/home/kasiro/Документы/jarvis/resources/commands/tests/test_core_api.py`
- `/home/kasiro/Документы/jarvis/resources/commands/tests/test_environment_api.py`
- `/home/kasiro/Документы/jarvis/resources/commands/tests/test_state_api.py`
- `/home/kasiro/Документы/jarvis/resources/commands/tests/test_modes_commands.py`

**Запуск тестов:**

```bash
cd /home/kasiro/Документы/jarvis/resources/commands
uv run pytest tests/ -v
```

---

## 8. Ключевые файлы

| Файл | Описание |
|------|----------|
| `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/__init__.py` | Главный экспорт API |
| `/home/kasiro/Документы/jarvis/resources/commands/jarvis_server.py` | Python RPC сервер |
| `/home/kasiro/Документы/jarvis/resources/commands/jarvis_api/environment.py` | Environment API |
| `/home/kasiro/Документы/jarvis/resources/commands/wayland.py` | WaylandController |
| `/home/kasiro/Документы/jarvis/resources/commands/wm_manager.py` | WindowManager, AppManager |
| `/home/kasiro/Документы/jarvis/crates/jarvis-core/src/commands.rs` | Rust интеграция Python |
| `/home/kasiro/Документы/jarvis/pyproject.toml` | Python зависимости |

---

## 9. Выводы

**Jarvis API полностью готов для расширения:**

1. ✅ **Модульная архитектура** - каждый API модуль независим
2. ✅ **Ленивая инициализация** - зависимости загружаются по требованию
3. ✅ **Кроссплатформенность** - поддержка Linux, Windows, macOS
4. ✅ **Асинхронность** - asyncio для HTTP и долгих операций
5. ✅ **Тестирование** - pytest тесты для API модулей
6. ✅ **Документация** - docstrings в каждом модуле

**Для работы с рабочими столами уже есть:**
- `switch_to_workspace(number)` - переключение
- `move_window_to_workspace(id, ws)` - перемещение окна
- `press_super_number(number)` - горячие клавиши

**Рекомендуется добавить:**
- `get_current_workspace()` - получение текущего рабочего стола
- `get_workspace_count()` - количество рабочих столов
- `next_workspace()` / `previous_workspace()` - навигация
- `get_windows_on_workspace(ws)` - список окон на рабочем столе

---

**🥒 Wubba Lubba Dub Dub! API изучено, Morty!**
