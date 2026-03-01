#!/usr/bin/env python3
"""Calculator OFF - закрывает калькулятор"""
import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis


async def execute(context):
    """Закрыть калькулятор"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Closing calculator...")
    
    # Закрываем калькулятор через exec_background
    jarvis.system.exec_background('killall gnome-calculator')
    
    return {"success": True}
