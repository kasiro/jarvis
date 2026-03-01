#!/usr/bin/env python3
"""Browser closer - закрывает браузер (Zen)"""
import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis


async def execute(context):
    """Закрыть браузер"""
    jarvis = init_jarvis(context)
    # jarvis.log("info", "Closing browser...")

    # Закрываем Zen браузер через exec_background
    jarvis.system.exec_background('killall zen-bin')

    return {"success": True}
