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
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

# Добавляем parent directory в path для импорта vpn
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from vpn import VPNController


async def open_youtube_kids_and_search():
    script_path = Path(__file__).parent / "rb.py"
    subprocess.Popen([sys.executable, str(script_path)])


async def execute(context):
    jarvis = init_jarvis(context)

    success = await jarvis.modes.set_mode("kid")

    if success:
        jarvis.audio.play_ok()
        delay = 0.5

        # 1. Запускаем VPN
        vpn = VPNController(server_index=1, cleanup=False)
        vpn_result = vpn.connect()
        jarvis.log("info", f"VPN status: {vpn_result}")

        # 2. Сворачиваем все окна
        jarvis.environment.minimize_all_windows()

        # 3. Запускаем браузер в фоне на активном рабочем столе
        await open_youtube_kids_and_search()

        # Уведомление
        # jarvis.system.notify("Kid Mode", "Детский режим активирован")

        return {"success": True}
    else:
        jarvis.log("error", "Failed to activate Kid Mode")
        jarvis.audio.play_error()
        jarvis.system.notify("Error", "Не удалось активировать детский режим")
        return {"success": False}
