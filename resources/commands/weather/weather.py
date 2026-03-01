#!/usr/bin/env python3
# weather command using wttr.in API with ansiweather fallback

import sys
import os
import subprocess
import json
import re
from jarvis_api import init_jarvis

# Get city from environment or use default
city = os.environ.get("JARVIS_CITY", "Novosibirsk")
lang = os.environ.get("JARVIS_LANG", "ru")

def send_notification(title, message):
    """Send desktop notification using notify-send"""
    try:
        subprocess.run(
            ["notify-send", title, message],
            timeout=5
        )
    except Exception:
        pass  # Notifications are optional

def fetch_weather_wttr(city, lang):
    """Fetch weather from wttr.in API"""
    import urllib.request
    import urllib.error

    # Try localized format
    url = f"http://wttr.in/{city}?format=3&lang={lang}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            body = response.read().decode('utf-8').strip()
            if body:
                return body
    except (urllib.error.URLError, Exception):
        pass

    return None

def fetch_weather_ansiweather(city):
    """Fetch weather using ansiweather CLI"""
    try:
        result = subprocess.run(
            ["ansiweather", "-l", f"{city},RU", "-u", "metric", "-f", "1", "-a", "false"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        pass

    return None


async def execute(context):
    """Get weather and show notification"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Fetching weather...")
    
    # Get city from context slots or use default
    city = context.get("slots", {}).get("city", os.environ.get("JARVIS_CITY", "Novosibirsk"))
    lang = context.get("language", "ru")
    
    # Method 1: wttr.in API
    weather = fetch_weather_wttr(city, lang)

    if weather:
        jarvis.log("info", f"Weather: {weather}")
        # Send notification with weather data
        jarvis.system.notify("Jarvis", f"{city}: {weather}")
        return {"success": True, "weather": weather}

    # Method 2: ansiweather fallback
    weather = fetch_weather_ansiweather(city)

    if weather:
        weather = weather.replace(' forecast', '')
        jarvis.log("info", f"Weather: {weather}")
        # Send notification with weather data
        jarvis.system.notify("Jarvis", f"{weather}")
        return {"success": True, "weather": weather}

    # Both methods failed
    jarvis.log("error", "Failed to fetch weather")
    jarvis.audio.play_error()
    return {"success": False, "error": "Failed to fetch weather"}


if __name__ == "__main__":
    # Legacy CLI mode
    weather = fetch_weather_wttr(city, lang)
    if weather:
        print(weather)
        send_notification("Jarvis", f"{city}: {weather}")
        sys.exit(0)
    
    weather = fetch_weather_ansiweather(city)
    if weather:
        print(weather)
        weather = weather.replace(' forecast', '')
        send_notification("Jarvis", f"{weather}")
        sys.exit(0)
    
    print("Failed to fetch weather", file=sys.stderr)
    sys.exit(1)
