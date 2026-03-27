#!/usr/bin/env python3
from time import sleep

import docker
from jarvis_api import init_jarvis


async def execute(context):
    """
    Выполнить команду

    Args:
        context: Контекст команды
    """
    # Инициализируем jarvis с контекстом
    jarvis = init_jarvis(context)

    jarvis.audio.play_ok()

    jarvis.system.exec('pkill -f "WebApp-Финансы9154"')

    return {"success": True}
