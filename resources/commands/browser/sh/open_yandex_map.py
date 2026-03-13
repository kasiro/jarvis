#!/usr/bin/env python3

import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api и wm_manager
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis


async def execute(context):
    jarvis = init_jarvis(context)
    jarvis.log("info", "Opening site [https://yandex.ru/maps/65/novosibirsk/]...")

    jarvis.system.exec("xdg-open", ["https://yandex.ru/maps/65/novosibirsk/"])
    jarvis.environment.press_super_number(1)

    jarvis.log("info", "site is ready")
    return {"success": True}
