#!/usr/bin/env python3
"""
Check Mode - Показывает текущий режим

Команды:
- "какой режим"
- "текущий режим"
- "покажи режим"
- "current mode"
"""
from jarvis_api import init_jarvis


async def execute(context):
    """
    Выполнить команду проверки текущего режима

    Args:
        context: Контекст команды
    """
    # Инициализируем jarvis с контекстом
    jarvis = init_jarvis(context)

    # Получаем текущий режим
    current_mode = jarvis.modes.get_current()

    jarvis.log("info", f"Current mode: {current_mode}")

    # Определяем описание режима
    mode_descriptions = {
        "normal": "Обычный режим",
        "kid": "Детский режим",
        "dev": "Режим разработчика"
    }

    description = mode_descriptions.get(current_mode, "Неизвестный режим")

    # Показываем уведомление
    jarvis.system.notify(
        "Current Mode",
        description
    )

    # Воспроизводим OK звук
    jarvis.audio.play_ok()

    return {"success": True}
