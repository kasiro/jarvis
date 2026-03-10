#!/usr/bin/env python3
"""IDE launcher - открывает редактор кода (Zed) или переключается на него"""

import sys
from pathlib import Path

# Добавляем parent directory в path для импорта jarvis_api
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis
from vpn import VPNController


async def execute(context):
    """убить VPN"""
    jarvis = init_jarvis(context)

    VPNController(cleanup=True)

    jarvis.log("info", "vpn closed")
    return {"success": True}
