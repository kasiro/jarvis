import ast
import json
import logging
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from subprocess import PIPE, Popen, check_call, check_output, run
from time import sleep
from typing import Any, Dict, List, Optional

# Добавляем parent directory в path для импорта wayland
parent_dir = str(Path(__file__).parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Исправленный импорт - используем относительный импорт внутри packages
from wayland import WaylandController

logger = logging.getLogger(__name__)


class WindowManager:
    """Управление окнами через D-Bus интерфейс window-calls@domandoman.xyz"""

    def __init__(self):
        self.dest = "org.gnome.Shell"
        self.path = "/org/gnome/Shell/Extensions/Windows"
        self.iface = "org.gnome.Shell.Extensions.Windows"

    def _call(self, method: str, *args) -> Any:
        """
        Вызывает D-Bus метод через gdbus и возвращает результат.
        """
        cmd = [
            "gdbus",
            "call",
            "--session",
            "--dest",
            self.dest,
            "--object-path",
            self.path,
            "--method",
            f"{self.iface}.{method}",
            *[str(arg) for arg in args],
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
        result = self._call("List")
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
                self._call("Minimize", str(w["id"]))
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
                self._call("Unminimize", str(w["id"]))
            except:
                success = False
        return success

    def _minimize_window(self, wm_class: str) -> bool:
        windows = self.get_windows()
        success = True
        for w in windows:
            try:
                if w["wm_class"] == wm_class:
                    self._call("Minimize", str(w["id"]))
            except:
                success = False
        return success

    def _maximize_window(self, wm_class: str) -> bool:
        windows = self.get_windows()
        success = True
        for w in windows:
            try:
                if w["wm_class"] == wm_class:
                    self._call("Maximize", str(w["id"]))
            except:
                success = False
        return success

    def _focus_window(self, wm_class: str) -> bool:
        windows = self.get_windows()
        success = True
        for w in windows:
            try:
                if w["wm_class"] == wm_class:
                    self._call("Activate", str(w["id"]))
            except:
                success = False
        return success

    def is_running(self, wm_class: str):
        windows = self.get_windows()
        wm_list = [wm["wm_class"] for wm in windows]
        if wm_class in wm_list:
            return True
        return False

    def get_window_id_wm_class(self, wm_class: str) -> int:
        windows = self.get_windows()
        for w in windows:
            if w["wm_class"] == wm_class:
                return w["id"]
        return 0

    def move_to_workspace(self, window_id: int, workspace: int) -> bool:
        """
        Перемещает окно с указанным ID на заданный рабочий стол.
        Возвращает True при успехе.
        """
        try:
            self._call("MoveToWorkspace", window_id, workspace)
            return True
        except Exception as e:
            logger.exception(f"Ошибка перемещения окна {window_id}")
            return False

    def move_to_workspace_wmclass(self, wmclass: str, workspace: int) -> bool:
        """
        Перемещает окно с указанным wmclass на заданный рабочий стол.
        Возвращает True при успехе.
        """
        self.wait_for_new_window_wmclass(wmclass)
        window_id = self.get_window_id_wm_class(wmclass)
        try:
            self._call("MoveToWorkspace", window_id, workspace)
            return True
        except Exception as e:
            logger.exception(f"Ошибка перемещения окна {wmclass}")
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

    def wait_for_new_window(
        self, before_ids: set, timeout: float = 10
    ) -> Optional[int]:
        """
        Ожидает появления нового окна, отсутствовавшего в before_ids.
        Возвращает ID нового окна или None.
        """
        start = time.time()
        while time.time() - start < timeout:
            windows = self.get_windows()
            current_ids = {w["id"] for w in windows}
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

    def __init__(self):
        self.wm = WindowManager()
        self.wayland = WaylandController()

    def launch(self, app_name: str, workspace: int) -> str:
        """
        Запускает приложение на указанном рабочем столе (блокирует).
        app_name: имя приложения (из APP_MAP)
        workspace: номер рабочего стола (0,1,2...)
        """
        workspace = workspace - 1

        cmd = shlex.split(app_name)

        try:
            # Получаем список окон ДО запуска
            before_windows = self.wm.get_windows()
            before_ids = {w["id"] for w in before_windows}

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

    def gtk_launch(self, app_name: str, workspace: int) -> str:
        """
        Запускает приложение на указанном рабочем столе (блокирует).
        app_name: имя приложения (из APP_MAP)
        workspace: номер рабочего стола (0,1,2...)
        """
        workspace = workspace - 1

        cmd = shlex.split("gtk-launch " + app_name)

        try:
            # Запускаем приложение
            subprocess.Popen(cmd)

            # Ждём появления нового окна
            if not self.wm.wait_for_new_window_wmclass(app_name, timeout=15):
                return f"❌ Не удалось найти окно для {app_name} после запуска."

            # Перемещаем на целевой рабочий стол
            if self.wm.move_to_workspace_wmclass(app_name, workspace):
                return f"✅ {app_name.capitalize()} запущен на рабочем столе {workspace + 1}"
            else:
                return f"❌ Не удалось переместить окно {app_name}."
        except Exception as e:
            logger.exception("Ошибка в launch")
            return f"❌ Ошибка: {str(e)}"

    def gtk_launch_background(self, app_name: str, workspace: int) -> str:
        """
        Запускает приложение на указанном рабочем столе (блокирует).
        app_name: имя приложения (из APP_MAP)
        workspace: номер рабочего стола (0,1,2...)
        """
        workspace = workspace - 1

        cmd = shlex.split("gtk-launch " + app_name)

        try:
            # Запускаем gtk приложение
            subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            # Ждём появления нового окна
            if not self.wm.wait_for_new_window_wmclass(app_name, timeout=15):
                return f"❌ Не удалось найти окно для {app_name} после запуска."

            # Перемещаем на целевой рабочий стол
            if self.wm.move_to_workspace_wmclass(app_name, workspace):
                self.wayland.press_super_number(workspace + 1)
                return f"✅ {app_name.capitalize()} запущен на рабочем столе {workspace + 1}"
            else:
                return f"❌ Не удалось переместить окно {app_name}."
        except Exception as e:
            logger.exception("Ошибка в launch")
            return f"❌ Ошибка: {str(e)}"

    def launch_background(self, app_name: str, wm_class: str, workspace: int) -> str:
        """
        Запускает приложение в фоне (не блокирует).
        app_name: имя приложения (из APP_MAP)
        workspace: номер рабочего стола (0,1,2...)
        """
        workspace = workspace - 1

        cmd = shlex.split(app_name)

        minimal_env = {
            "DISPLAY": os.environ.get("DISPLAY", ":0"),
            "WAYLAND_DISPLAY": os.environ.get("WAYLAND_DISPLAY", "wayland-0"),
            "XDG_RUNTIME_DIR": os.environ.get("XDG_RUNTIME_DIR"),
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "HOME": os.environ.get("HOME"),
            "LANG": os.environ.get("LANG", "ru_RU.UTF-8"),
        }
        minimal_env = {k: v for k, v in minimal_env.items() if v is not None}

        try:
            # Запускаем приложение в фоне
            subprocess.Popen(
                cmd,
                env=minimal_env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            # Перемещаем на целевой рабочий стол
            if self.wm.move_to_workspace_wmclass(wm_class, workspace):
                return f"✅ {app_name.capitalize()} запущен на рабочем столе {workspace + 1}"
            else:
                return f"❌ Не удалось переместить окно {app_name}."
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
            start_new_session=True,  # для Unix-систем
        )

    def launch_command_background(self, cmd: list[str]):
        """
        Запускает команду напрямую в фоне (без APP_MAP).
        cmd: список аргументов команды, например ["zed"] или ["firefox", "--new-window"]
        """
        try:
            Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return f"✅ Команда запущена: {' '.join(cmd)}"
        except Exception as e:
            logger.exception("Ошибка в launch_command_background")
            return f"❌ Ошибка: {str(e)}"

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
            self.launcher.launch_background(appname, wm_class, workspace)
            self.wayland.press_super_number(workspace)
            return

        # Переключаемся на рабочий стол
        self.wayland.press_super_number(workspace)
