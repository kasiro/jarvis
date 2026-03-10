#!/usr/bin/env python3
"""
Kid Mode ON - Включает детский режим

Команды:
- "детский режим"
- "запусти детский режим"
- "протокол мультики"
- "kid mode"

Функции детского режима:
- Запускает VPN (безопасное соединение)
- Сворачивает все окна (родительский контроль)
- Открывает YouTube Kids в Firefox
"""

import sys
from pathlib import Path
from time import sleep

from jarvis_api import init_jarvis

# Добавляем parent directory в path для импорта vpn
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from vpn import VPNController


def setup(jarvis, delay):
    sleep(18)

    # Настойка

    # принять
    jarvis.environment.press_tab(2)
    jarvis.environment.press_enter()

    sleep(delay)

    # согласиться
    jarvis.environment.press_tab()
    jarvis.environment.press_enter()

    sleep(delay)

    for num in [2, 0, 0, 3]:
        jarvis.environment.press_number(num)
    jarvis.environment.press_enter()
    sleep(delay)
    jarvis.environment.press_space()
    jarvis.environment.press_tab(6)
    jarvis.environment.press_enter()
    sleep(delay)
    jarvis.environment.press_tab(2)
    jarvis.environment.press_enter()
    sleep(delay)
    jarvis.environment.press_tab(3)
    jarvis.environment.press_enter()
    sleep(delay)
    jarvis.environment.press_tab(5)
    jarvis.environment.press_enter()

    sleep(delay)
    jarvis.environment.press_tab()
    jarvis.environment.press_enter()

    sleep(delay)
    jarvis.environment.press_tab()
    jarvis.environment.press_enter()

    sleep(delay)
    jarvis.environment.press_tab(2)
    jarvis.environment.press_enter()

    sleep(delay)
    jarvis.environment.press_tab(2)
    jarvis.environment.press_enter()


async def execute(context):
    """
    Выполнить команду включения детского режима

    Args:
        context: Контекст команды
    """
    # Инициализируем jarvis с контекстом
    jarvis = init_jarvis(context)

    # jarvis.log("info", "Activating Kid Mode...")

    # Переключаем режим
    success = await jarvis.modes.set_mode("kid")

    if success:
        # jarvis.log("info", "Kid Mode activated successfully")
        jarvis.audio.play_ok()

        # 1. Запускаем VPN через VPNController (без cleanup для скорости)
        # jarvis.log("info", "Starting VPN for kid safety...")
        vpn = VPNController(server_index=1, cleanup=False)
        vpn_result = vpn.connect()
        # jarvis.log("info", f"VPN status: {vpn_result}")

        # 2. Сворачиваем все окна (чтобы ребёнок не видел лишнего)
        # jarvis.log("info", "Minimizing all windows for kid safety...")
        jarvis.environment.minimize_all_windows()

        # 3. Открываем YouTube Kids (фоновый запуск)
        # jarvis.log("info", "Opening YouTube Kids...")
        jarvis.system.exec_background("gtk-launch WebApp-youtubekids8701")
        not_found = 10
        interval = 0.5
        count = 0
        delay = 0.5

        while True:
            is_run = jarvis.environment.is_app_running("WebApp-youtubekids8701")
            if is_run:
                jarvis.environment.focus_window("WebApp-youtubekids8701")
                # jarvis.environment.maximize_window("WebApp-youtubekids8701")
                break
            sleep(interval)
            count += 0.5

            if round((count * interval), 0) >= not_found:
                break

        # setup(jarvis, delay)
        sleep(6)

        sleep(delay)
        jarvis.environment.press_tab(3)
        jarvis.environment.type_text("синий трактор")
        jarvis.environment.press_enter()

        sleep(delay)
        jarvis.environment.press_tab()
        sleep(delay)
        jarvis.environment.press_enter()

        sleep(delay)
        jarvis.environment.press_tab(7)
        sleep(delay)
        jarvis.environment.press_enter()

        # Показываем уведомление
        # jarvis.system.notify("Kid Mode", "Детский режим активирован")

        return {"success": True}
    else:
        jarvis.log("error", "Failed to activate Kid Mode")
        jarvis.audio.play_error()
        jarvis.system.notify("Error", "Не удалось активировать детский режим")

        return {"success": False, "error": "Failed to activate Kid Mode"}
