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
    jarvis = init_jarvis(context)
    jarvis.environment.press_space()
    jarvis.environment.type_text_english("truerealyexp")
    jarvis.environment.press_enter()

    return {"success": True}
