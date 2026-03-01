#!/usr/bin/env python3
"""
Kid Mode OFF - Выключает детский режим

Команды:
- "обычный режим"
- "выключи детский режим"
- "деактивируй детский режим"
- "normal mode"

Функции выключения детского режима:
- Останавливает VPN через VPNController
- Закрывает YouTube Kids
- Разворачивает окна обратно
"""
from jarvis_api import init_jarvis
import sys
from pathlib import Path

# Добавляем parent directory в path для импорта vpn
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from vpn import VPNController


async def execute(context):
    """
    Выполнить команду выключения детского режима

    Args:
        context: Контекст команды
    """
    # Инициализируем jarvis с контекстом
    jarvis = init_jarvis(context)

    # jarvis.log("info", "Deactivating Kid Mode...")

    # Переключаем режим
    success = await jarvis.modes.set_mode("normal")

    if success:
        # jarvis.log("info", "Normal mode activated successfully")

        # Воспроизводим OK звук
        jarvis.audio.play_ok()

        # 1. Останавливаем VPN через VPNController
        # jarvis.log("info", "Stopping VPN...")
        vpn = VPNController(server_index=0, cleanup=False)
        vpn_result = vpn.disconnect()
        # jarvis.log("info", f"VPN status: {vpn_result}")

        # 2. Закрываем Firefox с YouTube Kids
        # jarvis.log("info", "Closing YouTube Kids...")
        jarvis.system.exec("pkill -f 'firefox.*youtubekids'")

        # 3. Разворачиваем все окна обратно
        # jarvis.log("info", "Restoring windows...")
        jarvis.environment.maximize_all_windows()

        # Показываем уведомление
        # jarvis.system.notify(
        #     "Normal Mode",
        #     "Обычный режим активирован"
        # )

        return {"success": True}
    else:
        jarvis.log("error", "Failed to deactivate Kid Mode")
        jarvis.audio.play_error()
        jarvis.system.notify(
            "Error",
            "Не удалось деактивировать детский режим"
        )

        return {"success": False, "error": "Failed to deactivate Kid Mode"}
