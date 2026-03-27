#!/usr/bin/env python3

import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api и wm_manager
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis

# маршрут
# https://yandex.ru/maps/?rtext=Новосибирск, {FROM}~Новосибирск, {TO}


async def execute(context):
    jarvis = init_jarvis(context)
    addr = context.get("slots", {}).get("addr", "")
    jarvis.log("info", f"Opening address [{addr}]...")
    if addr != "":
        jarvis.audio.play_ok()
        jarvis.log("info", f"Opening address [{addr}]...")

        jarvis.system.open(f"https://yandex.ru/maps/?text={addr}")
        jarvis.environment.press_super_number(1)

        jarvis.log("info", "addr is ready")
        return {"success": True}
    else:
        jarvis.log("info", f"error: no address, context: {str(context)}")
        return {"success": False, "error": "no address"}
