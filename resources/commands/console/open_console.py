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

    # jarvis.system.notify("jarvis", "Консоль запущена")

    jarvis.log("info", "console is ready")
    return {"success": True}
