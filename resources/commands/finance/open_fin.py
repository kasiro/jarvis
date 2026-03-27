#!/usr/bin/env python3
from time import sleep

import docker
from jarvis_api import init_jarvis


def ensure_container_running(container_name):
    client = docker.from_env()
    try:
        container = client.containers.get(container_name)
        if container.status == "running":
            print(f"Контейнер {container_name} уже запущен.")
        else:
            print(f"Контейнер {container_name} остановлен. Запускаем...")
            container.start()
            # Обновляем статус после запуска
            container.reload()
            print(f"Контейнер {container_name} запущен. Статус: {container.status}")
        return container
    except docker.errors.NotFound:  # type: ignore
        pass


async def execute(context):
    """
    Выполнить команду

    Args:
        context: Контекст команды
    """
    # Инициализируем jarvis с контекстом
    jarvis = init_jarvis(context)

    jarvis.audio.play_ok()

    ensure_container_running("ezbookkeeping")

    jarvis.environment.gtk_launch_background("WebApp-Финансы9154", 2)

    return {"success": True}
