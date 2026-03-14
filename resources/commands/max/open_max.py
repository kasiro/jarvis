#!/usr/bin/env python3
"""
Kid Mode ON - Включает детский режим (версия с Playwright)

Команды:
- "детский режим"
- "запусти детский режим"
- "протокол мультики"
- "kid mode"

Функции детского режима:
- Запускает VPN (безопасное соединение)
- Сворачивает все окна (родительский контроль)
- Открывает YouTube Kids в Firefox и выполняет настройки
"""

import asyncio
import subprocess
import sys
from pathlib import Path
from time import sleep

from jarvis_api import init_jarvis

# Добавляем parent directory в path для импорта vpn
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


async def open_max():
    script_path = Path(__file__).parent / "max.py"
    subprocess.Popen([sys.executable, str(script_path)])


async def execute(context):
    jarvis = init_jarvis(context)

    jarvis.audio.play_ok()
    delay = 0.5

    # 2. Сворачиваем все окна
    jarvis.environment.minimize_all_windows()

    # 3. Запускаем браузер в фоне на активном рабочем столе
    await open_max()

    return {"success": True}
