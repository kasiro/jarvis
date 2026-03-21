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

from time import sleep

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

        # FIX: при запуске kgx запускается вместе с активированым venv
        # FIX: долго запускает zeditor и запускает на текущем раб столе а надо на указанном

        jarvis.environment.launch_or_move_app_background("firefox", "firefox", 1)
        jarvis.environment.wait_for_new_window_wmclass("firefox")

        jarvis.environment.launch_or_move_app_background(
            "kgx --working-directory '/home/kasiro/'", "org.gnome.Console", 2
        )
        jarvis.environment.wait_for_new_window_wmclass("org.gnome.Console")
        jarvis.environment.launch_or_move_app_background("zeditor", "dev.zed.Zed", 3)
        jarvis.environment.wait_for_new_window_wmclass("dev.zed.Zed")
        jarvis.environment.gtk_launch_background("WebApp-yougile3417", 4)
        jarvis.environment.wait_for_new_window_wmclass("WebApp-yougile3417")

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
