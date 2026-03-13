#!/usr/bin/env python3

import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api и wm_manager
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from time import sleep

from jarvis_api import init_jarvis


async def execute(context):
    """Открыть браузер или переключиться на него"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Opening console...")

    jarvis.environment.launch_or_move_app_background(
        "kgx --working-directory '/home/kasiro/'", "org.gnome.Console", 2
    )

    # timeout = 5
    # t = 0
    # while True:
    #     running = jarvis.environment.is_app_running("org.gnome.Console")
    #     if running:
    #         # jarvis.environment.maximize_window("org.gnome.Console")
    #         jarvis.environment.press_super_number(2)
    #         break

    #     if t >= timeout:
    #         break

    #     sleep(1)
    #     t += 1

    # jarvis.system.notify("jarvis", "Консоль запущена")

    jarvis.log("info", "console is ready")
    return {"success": True}
