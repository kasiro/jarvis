#!/usr/bin/env python3
"""IDE launcher - открывает редактор кода (Zed) или переключается на него"""
import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api и wm_manager
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis
from wm_manager import AppManager


async def execute(context):
    """Открыть редактор кода или переключиться на него"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Opening IDE...")
    
    # Используем AppManager для умного запуска (не блокирует)
    manager = AppManager()
    manager.launch_or_move_background('zed', 'dev.zed.Zed', 3)
    
    jarvis.log("info", "IDE ready")
    return {"success": True}
