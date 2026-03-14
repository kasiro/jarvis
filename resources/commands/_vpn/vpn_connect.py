#!/usr/bin/env python3

import sys
from pathlib import Path
from time import sleep

# Добавляем parent directory в path для импорта jarvis_api
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from jarvis_api import init_jarvis
from vpn import VPNController


async def execute(context):
    """Запустить VPN"""
    jarvis = init_jarvis(context)

    vpn = VPNController(server_index=1, cleanup=False)
    if not vpn.is_connected():
        vpn.connect()
        sleep(0.5)

    jarvis.environment.minimize_window("AmneziaVPN")

    jarvis.log("info", "vpn is ready")
    return {"success": True}
