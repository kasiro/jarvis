#!/usr/bin/env python3
"""
Dev Mode ON - Включает режим разработчика

Команды:
- "режим разработчика"
- "dev режим"
- "включи режим разработчика"
- "dev mode"

Функции режима разработчика:
- Управление рабочими столами
- Быстрый запуск приложений (Zen, Zed)
- Развёрнутые окна
"""

from jarvis_api import init_jarvis


async def execute(context):
    """
    Выполнить команду включения режима разработчика

    Args:
        context: Контекст команды
    """
    # Инициализируем jarvis с контекстом
    jarvis = init_jarvis(context)

    jarvis.log("info", "Activating Dev Mode...")

    # Переключаем режим
    success = await jarvis.modes.set_mode("dev")

    if success:
        jarvis.log("info", "Dev Mode activated successfully")

        # СРАЗУ воспроизводим OK звук (сразу после получения команды!)
        jarvis.audio.play_ok()

        # Разворачиваем все окна (для удобной разработки)
        jarvis.log("info", "Maximizing all windows for dev workspace...")
        jarvis.environment.launch_app("firefox", 1)
        jarvis.environment.launch_app("kgx --working-directory '/home/kasiro/'", 2)
        jarvis.environment.launch_app("zeditor", 3)
        # jarvis.environment.gtk_launch_app('')

        # Показываем уведомление
        # jarvis.system.notify(
        #     "Dev Mode",
        #     "Режим разработчика активирован!"
        # )

        return {"success": True}
    else:
        jarvis.log("error", "Failed to activate Dev Mode")
        jarvis.audio.play_error()
        jarvis.system.notify("Error", "Не удалось активировать режим разработчика")

        return {"success": False, "error": "Failed to activate Dev Mode"}
