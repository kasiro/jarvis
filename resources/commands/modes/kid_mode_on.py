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

from jarvis_api import init_jarvis

# Добавляем parent directory в path для импорта vpn
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from vpn import VPNController


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

        # Воспроизводим OK звук
        jarvis.audio.play_ok()

        # 1. Запускаем VPN через VPNController (без cleanup для скорости)
        # jarvis.log("info", "Starting VPN for kid safety...")
        vpn = VPNController(server_index=0, cleanup=False)
        vpn_result = vpn.connect()
        # jarvis.log("info", f"VPN status: {vpn_result}")

        # 2. Сворачиваем все окна (чтобы ребёнок не видел лишнего)
        # jarvis.log("info", "Minimizing all windows for kid safety...")
        jarvis.environment.minimize_all_windows()

        # 3. Открываем YouTube Kids в Firefox (фоновый запуск)
        # jarvis.log("info", "Opening YouTube Kids...")
        jarvis.system.exec_background('firefox --new-window https://www.youtubekids.com/?hl=ru')



        # Показываем уведомление
        # jarvis.system.notify(
        #     "Kid Mode",
        #     "Детский режим активирован"
        # )

        return {"success": True}
    else:
        jarvis.log("error", "Failed to activate Kid Mode")
        jarvis.audio.play_error()
        jarvis.system.notify(
            "Error",
            "Не удалось активировать детский режим"
        )

        return {"success": False, "error": "Failed to activate Kid Mode"}
