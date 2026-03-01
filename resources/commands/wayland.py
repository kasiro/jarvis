import os
import sys
from pathlib import Path

# Добавляем текущую директорию в path для импорта pydotool
current_dir = str(Path(__file__).parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Пытаемся импортировать pydotool
# При запуске через 'uv run' .venv уже в sys.path, поэтому просто импортируем
pydotool = None
KEY_LEFTMETA = KEY_1 = KEY_2 = KEY_3 = KEY_4 = KEY_L = None

try:
    import pydotool
    from pydotool import KEY_LEFTMETA, KEY_1, KEY_2, KEY_3, KEY_4, KEY_L
except ImportError:
    # pydotool не найден - пробуем добавить .venv вручную и импортировать через importlib
    try:
        venv_path = Path('/home/kasiro/Документы/jarvis/.venv') / 'lib'
        if venv_path.exists():
            for site_packages in venv_path.glob('*/site-packages'):
                sp_str = str(site_packages)
                if sp_str not in sys.path:
                    sys.path.append(sp_str)
                break
        
        # Используем importlib для повторного импорта
        import importlib
        pydotool = importlib.import_module('pydotool')
        KEY_LEFTMETA = getattr(pydotool, 'KEY_LEFTMETA', None)
        KEY_1 = getattr(pydotool, 'KEY_1', None)
        KEY_2 = getattr(pydotool, 'KEY_2', None)
        KEY_3 = getattr(pydotool, 'KEY_3', None)
        KEY_4 = getattr(pydotool, 'KEY_4', None)
        KEY_L = getattr(pydotool, 'KEY_L', None)
    except ImportError:
        # pydotool не установлен - используем заглушки
        pass

class WaylandController:
    def __init__(self):
        self.pydotool = pydotool
        if pydotool:
            os.environ['YDOTOOL_SOCKET'] = '/run/user/1000/.ydotool_socket'
            # Инициализируем pydotool
            pydotool.init()
        self.num_keys = {
            1: KEY_1,
            2: KEY_2,
            3: KEY_3,
            4: KEY_4
        }

    def press_super_number(self, number: int):
        """Нажать комбинацию Super + цифра (number от 0 до 9)."""
        if not self.pydotool:
            raise RuntimeError("pydotool не установлен")
        if number not in self.num_keys:
            raise ValueError(f"Неверная цифра: {number}. Допустимо от 0 до 9.")
        self.pydotool.key_combination([KEY_LEFTMETA, self.num_keys[number]])
