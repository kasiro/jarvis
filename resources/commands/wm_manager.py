from subprocess import run, check_output, check_call, Popen, PIPE
import subprocess
from time import sleep
import json
import time
import logging
import ast
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any

# Добавляем parent directory в path для импорта wayland
parent_dir = str(Path(__file__).parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Исправленный импорт - используем относительный импорт внутри packages
from wayland import WaylandController

logger = logging.getLogger(__name__)

class WindowManager:
    """Управление окнами через D-Bus интерфейс Window Calls."""

    def __init__(self):
        self.dest = 'org.gnome.Shell'
        self.path = '/org/gnome/Shell/Extensions/Windows'
        self.iface = 'org.gnome.Shell.Extensions.Windows'

    def _call(self, method: str, *args) -> Any:
        """
        Вызывает D-Bus метод через gdbus и возвращает результат.
        """
        cmd = [
            'gdbus', 'call', '--session',
            '--dest', self.dest,
            '--object-path', self.path,
            '--method', f'{self.iface}.{method}',
            *[str(arg) for arg in args]
        ]
        try:
            output = check_output(cmd, stderr=PIPE, text=True)
            output = output.strip()
            # gdbus возвращает кортеж в виде строки, например: (true, '...') или просто ('значение',)
            # Парсим через ast.literal_eval и извлекаем первый элемент, если это кортеж.
            try:
                parsed = ast.literal_eval(output)
                if isinstance(parsed, tuple):
                    # Берём первый элемент (он может быть строкой, числом и т.д.)
                    return parsed[0]
                else:
                    return parsed
            except:
                # Если не удалось распарсить, возвращаем как есть
                return output
        except subprocess.CalledProcessError as e:
            logger.error(f"Ошибка D-Bus вызова {method}: {e.stderr}")
            raise

    def get_windows(self) -> List[Dict]:
        """
        Возвращает список всех окон с их свойствами.
        """
        result = self._call('List')
        try:
            windows = json.loads(result)
            return windows
        except json.JSONDecodeError:
            logger.error(f"Не удалось распарсить JSON: {result}")
            return []

    def _minimize_all_manually(self) -> bool:
        """
        Сворачивает каждое окно по очереди (если нет специального метода).
        """
        windows = self.get_windows()
        success = True
        for w in windows:
            try:
                self._call('Minimize', str(w['id']))
            except:
                success = False
        return success

    def _maximize_all_manually(self) -> bool:
        """
        Сворачивает каждое окно по очереди (если нет специального метода).
        """
        windows = self.get_windows()
        success = True
        for w in windows:
            try:
                self._call('Unminimize', str(w['id']))
            except:
                success = False
        return success

    def is_running(self, wm_class: str):
        windows = self.get_windows()
        wm_list = [wm['wm_class'] for wm in windows]
        if wm_class in wm_list:
                return True
        return False


    def move_to_workspace(self, window_id: int, workspace: int) -> bool:
        """
        Перемещает окно с указанным ID на заданный рабочий стол.
        Возвращает True при успехе.
        """
        try:
            self._call('MoveToWorkspace', window_id, workspace)
            return True
        except Exception as e:
            logger.exception(f"Ошибка перемещения окна {window_id}")
            return False

    def wait_for_new_window_wmclass(self, wmclass: str, timeout: float = 10) -> bool:
        """
        Ожидает появления нового окна.
        Возвращает True или False.
        """
        start = time.time()
        while time.time() - start < timeout:
            if self.is_running(wmclass):
                return True
            sleep(0.3)
        return False

    def wait_for_new_window(self, before_ids: set, timeout: float = 10) -> Optional[int]:
        """
        Ожидает появления нового окна, отсутствовавшего в before_ids.
        Возвращает ID нового окна или None.
        """
        start = time.time()
        while time.time() - start < timeout:
            windows = self.get_windows()
            current_ids = {w['id'] for w in windows}
            new_ids = current_ids - before_ids
            if new_ids:
                return next(iter(new_ids))
            time.sleep(0.3)
        return None


class AppLauncher:
    """Запуск приложений на указанных рабочих столах."""

    # Соответствие имени приложения команде и классу окна
    # wm_class берётся из D-Bus: gdbus call --session --dest org.gnome.Shell \
    #   --object-path /org/gnome/Shell/Extensions/Windows \
    #   --method org.gnome.Shell.Extensions.Windows.List
    APP_MAP = {
        'zen-browser': {'cmd': ['zen-browser'], 'class': 'zen'},
        'zed': {'cmd': ['zed'], 'class': 'dev.zed.Zed'},
        'calculator': {'cmd': ['gnome-calculator'], 'class': 'org.gnome.Calculator'},
    }

    def __init__(self):
        self.wm = WindowManager()

    def launch(self, app_name: str, workspace: int, **kwargs) -> str:
        """
        Запускает приложение на указанном рабочем столе (блокирует).
        app_name: имя приложения (из APP_MAP)
        workspace: номер рабочего стола (0,1,2...)
        """
        workspace = workspace - 1

        app_info = self.APP_MAP.get(app_name.lower())
        if not app_info:
            return f"❌ Неизвестное приложение: {app_name}. Доступны: {', '.join(self.APP_MAP.keys())}"

        cmd = app_info['cmd']

        try:
            # Получаем список окон ДО запуска
            before_windows = self.wm.get_windows()
            before_ids = {w['id'] for w in before_windows}

            # Запускаем приложение
            subprocess.Popen(cmd)

            # Ждём появления нового окна
            new_id = self.wm.wait_for_new_window(before_ids, timeout=15)
            if new_id is None:
                return f"❌ Не удалось найти окно для {app_name} после запуска."

            # Перемещаем на целевой рабочий стол
            if self.wm.move_to_workspace(new_id, workspace):
                display_workspace = workspace + 1
                return f"✅ {app_name.capitalize()} запущен на рабочем столе {display_workspace}"
            else:
                return f"❌ Не удалось переместить окно {app_name}."
        except Exception as e:
            logger.exception("Ошибка в launch")
            return f"❌ Ошибка: {str(e)}"

    def launch_background(self, app_name: str, workspace: int, **kwargs) -> str:
        """
        Запускает приложение в фоне (не блокирует).
        app_name: имя приложения (из APP_MAP)
        workspace: номер рабочего стола (0,1,2...)
        """
        workspace = workspace - 1

        app_info = self.APP_MAP.get(app_name.lower())
        if not app_info:
            return f"❌ Неизвестное приложение: {app_name}. Доступны: {', '.join(self.APP_MAP.keys())}"

        cmd = app_info['cmd']

        try:
            # Запускаем приложение в фоне
            subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

            # Не ждём появления окна - возвращаем сразу
            display_workspace = workspace + 1
            return f"✅ {app_name.capitalize()} запущен на рабочем столе {display_workspace}"
        except Exception as e:
            logger.exception("Ошибка в launch_background")
            return f"❌ Ошибка: {str(e)}"


class AppManager:

    def __init__(self):
        self.launcher = AppLauncher()
        self.wayland = WaylandController()
        self.windowManager = WindowManager()

    def execute(self, args: list[str]):
        run(args)

    def execute_background(self, args: list[str]):
        Popen(
            args,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # для Unix-систем
        )

    def maximize_all_windows(self) -> bool:
        return self.windowManager._maximize_all_manually()

    def minimize_all_windows(self) -> bool:
        return self.windowManager._minimize_all_manually()

    def launch_or_move(self, appname: str, wm_class: str, workspace: int):
        """
        Запускает приложение или переключается на него (блокирует до появления окна).
        """
        if not self.windowManager.is_running(wm_class):
            self.launcher.launch(appname, workspace)
            is_running = self.windowManager.wait_for_new_window_wmclass(wm_class)
            if is_running:
                self.wayland.press_super_number(workspace)

        self.wayland.press_super_number(workspace)

    def launch_or_move_background(self, appname: str, wm_class: str, workspace: int):
        """
        Запускает приложение в фоне или переключается на него (не блокирует).
        """
        if not self.windowManager.is_running(wm_class):
            # Запускаем в фоне
            self.launcher.launch_background(appname, workspace)
            # Не ждём появления окна
        
        # Переключаемся на рабочий стол
        self.wayland.press_super_number(workspace)
