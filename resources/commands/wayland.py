import os
import sys
from pathlib import Path
from subprocess import run
from time import sleep

# Добавляем текущую директорию в path для импорта pydotool
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Пытаемся импортировать pydotool
# При запуске через 'uv run' .venv уже в sys.path, поэтому просто импортируем
pydotool = None
KEY_LEFTMETA = KEY_V = KEY_LEFTCTRL = KEY_SPACE = KEY_0 = KEY_1 = KEY_2 = KEY_3 = (
    KEY_4
) = KEY_L = KEY_TAB = KEY_ENTER = None

try:
    import pydotool
    from pydotool import (
        KEY_0,
        KEY_1,
        KEY_2,
        KEY_3,
        KEY_4,
        KEY_ENTER,
        KEY_L,
        KEY_LEFTCTRL,
        KEY_LEFTMETA,
        KEY_SPACE,
        KEY_TAB,
        KEY_V,
    )
except ImportError:
    # pydotool не найден - пробуем добавить .venv вручную и импортировать через importlib
    try:
        venv_path = Path("/home/kasiro/Документы/jarvis/.venv") / "lib"
        if venv_path.exists():
            for site_packages in venv_path.glob("*/site-packages"):
                sp_str = str(site_packages)
                if sp_str not in sys.path:
                    sys.path.append(sp_str)
                break

        # Используем importlib для повторного импорта
        import importlib

        pydotool = importlib.import_module("pydotool")
        KEY_LEFTMETA = getattr(pydotool, "KEY_LEFTMETA", None)
        KEY_0 = getattr(pydotool, "KEY_0", None)
        KEY_1 = getattr(pydotool, "KEY_1", None)
        KEY_2 = getattr(pydotool, "KEY_2", None)
        KEY_3 = getattr(pydotool, "KEY_3", None)
        KEY_4 = getattr(pydotool, "KEY_4", None)
        KEY_L = getattr(pydotool, "KEY_L", None)
        KEY_TAB = getattr(pydotool, "KEY_TAB", None)
        KEY_ENTER = getattr(pydotool, "KEY_ENTER", None)
        KEY_SPACE = getattr(pydotool, "KEY_SPACE", None)
        KEY_LEFTCTRL = getattr(pydotool, "KEY_LEFTCTRL", None)
        KEY_V = getattr(pydotool, "KEY_V", None)
    except ImportError:
        # pydotool не установлен - используем заглушки
        pass


class WaylandController:
    def __init__(self):
        self.pydotool = pydotool
        if pydotool:
            os.environ["YDOTOOL_SOCKET"] = "/run/user/1000/.ydotool_socket"
            # Инициализируем pydotool
            pydotool.init()
        self.num_keys = {0: KEY_0, 1: KEY_1, 2: KEY_2, 3: KEY_3, 4: KEY_4}

    def press_enter(self):
        """Нажать Enter"""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        self.pydotool.key_combination([KEY_ENTER])  # type: ignore

    def type_text(self, text: str):
        """напечатать текст через ctrl-C + ctrl-V"""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        run(["wl-copy", text])
        # sleep(0.1)
        self.pydotool.key_combination([KEY_LEFTCTRL, KEY_V])  # type: ignore

    def type_text_english(self, text: str, char_delay_ms=50, hold_delay_ms=30):
        """напечатать текст (English only)"""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        self.pydotool.type_string(
            text, each_char_delay_ms=char_delay_ms, hold_delay_ms=hold_delay_ms
        )

    def press_tab(self, count: int = 1, delay=0.1):
        """Нажать Tab. $count раз"""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        if count > 1:
            for i in range(count):
                self.pydotool.key_combination([KEY_TAB])  # type: ignore
                sleep(delay)
        else:
            self.pydotool.key_combination([KEY_TAB])  # type: ignore

    def press_space(self):
        """Нажать комбинацию цифра (number от 0 до 4)."""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        self.pydotool.key_combination([KEY_SPACE])  # type: ignore

    def press_number(self, number: int):
        """Нажать комбинацию цифра (number от 0 до 4)."""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        if number not in self.num_keys:
            raise ValueError(f"Неверная цифра: {number}. Допустимо от 0 до 4.")
        self.pydotool.key_combination([self.num_keys[number]])  # type: ignore

    def press_super_number(self, number: int):
        """Нажать комбинацию Super + цифра (number от 0 до 4)."""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        if number not in self.num_keys:
            raise ValueError(f"Неверная цифра: {number}. Допустимо от 0 до 4.")
        self.pydotool.key_combination([KEY_LEFTMETA, self.num_keys[number]])  # type: ignore
