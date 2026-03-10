#!/usr/bin/env python3
"""IDE launcher - открывает редактор кода (Zed) или переключается на него"""

import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis


async def execute(context):
    """Открыть редактор кода (Zed) или переключиться на него"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Opening IDE...")

    jarvis.environment.launch_or_move_app("zeditor", "dev.zed.Zed", 3)

    jarvis.log("info", "IDE ready")
    return {"success": True}
