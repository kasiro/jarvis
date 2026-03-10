#!/usr/bin/env python3
"""Browser launcher - открывает браузер или переключается на него"""

import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api и wm_manager
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis


async def execute(context):
    """Открыть браузер или переключиться на него"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Opening browser...")

    jarvis.environment.launch_or_move_app("firefox", "firefox", 1)

    jarvis.log("info", "Browser ready")
    return {"success": True}
