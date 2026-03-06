#!/usr/bin/env python3
# weather command using wttr.in API with open-meteo fallback

import json
import os
import re
import subprocess
import sys

from jarvis_api import init_jarvis

# Get city from environment or use default
city = os.environ.get("JARVIS_CITY", "Novosibirsk")
lang = os.environ.get("JARVIS_LANG", "ru")

# City coordinates for open-meteo (fallback)
CITY_COORDS = {
    "novosibirsk": (55.0084, 82.9357),
}


def send_notification(title, message):
    """Send desktop notification using notify-send"""
    try:
        subprocess.run(
            ["notify-send", title, message, "-t", "5000"],
            timeout=5,
            capture_output=True,
        )
    except Exception as e:
        pass


def fetch_weather_wttr(city, lang):
    """Fetch weather from wttr.in API"""
    import urllib.error
    import urllib.request

    # Try localized format
    url = f"http://wttr.in/{city}?format=3&lang={lang}"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            body = response.read().decode("utf-8").strip()
            if body and "Unknown location" not in body:
                return body
    except (urllib.error.URLError, TimeoutError, Exception) as e:
        pass

    return None


def fetch_weather_openmeteo(city, lang):
    """Fetch weather from open-meteo.com API (fallback)"""
    import urllib.error
    import urllib.request

    # Get coordinates
    city_lower = city.lower()
    coords = CITY_COORDS.get(city_lower, (55.0084, 82.9357))  # Default: Novosibirsk
    lat, lon = coords

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            current = data.get("current_weather", {})

            if current:
                temp = current.get("temperature", "?")
                wind = current.get("windspeed", "?")
                code = current.get("weathercode", 0)

                # Weather code to icon/description
                weather_descriptions = {
                    0: "Ясно",
                    1: "Преимущественно ясно",
                    2: "Облачно",
                    3: "Пасмурно",
                    45: "Туман",
                    48: "Туман с инеем",
                    51: "Морось",
                    53: "Умеренная морось",
                    55: "Плотная морось",
                    61: "Дождь",
                    63: "Умеренный дождь",
                    65: "Сильный дождь",
                    71: "Снег",
                    73: "Умеренный снег",
                    75: "Сильный снег",
                    95: "Гроза",
                    96: "Гроза с градом",
                    99: "Сильная гроза с градом",
                }

                description = weather_descriptions.get(code, "Неизвестно")
                return f"{description}, {temp}°C, ветер {wind} м/с"

    except (urllib.error.URLError, TimeoutError, Exception) as e:
        pass

    return None


async def execute(context):
    """Get weather and show notification"""
    jarvis = init_jarvis(context)
    jarvis.log("info", "Fetching weather...")

    # Get city from context slots or use default
    city = context.get("slots", {}).get(
        "city", os.environ.get("JARVIS_CITY", "Novosibirsk")
    )
    lang = context.get("language", "ru")

    # Method 1: wttr.in API
    weather = fetch_weather_wttr(city, lang)

    if weather:
        jarvis.log("info", f"Weather: {weather}")
        # Send notification with weather data
        jarvis.system.notify("🥒 Jarvis", f"{city}: {weather}")
        jarvis.audio.play_ok()
        return {"success": True, "weather": weather}

    # Method 2: open-meteo.com fallback
    weather = fetch_weather_openmeteo(city, lang)

    if weather:
        jarvis.log("info", f"Weather: {weather}")
        # Send notification with weather data
        jarvis.system.notify("🥒 Jarvis", f"{city}: {weather}")
        jarvis.audio.play_ok()
        return {"success": True, "weather": weather}

    # Both methods failed
    jarvis.log("error", "Failed to fetch weather")
    jarvis.audio.play_error()
    jarvis.system.notify("🥒 Jarvis", "Не удалось получить погоду. Проверьте интернет.")
    return {"success": False, "error": "Failed to fetch weather"}


if __name__ == "__main__":
    # Legacy CLI mode
    weather = fetch_weather_wttr(city, lang)
    if weather:
        print(weather)
        send_notification("Jarvis", f"{city}: {weather}")
        sys.exit(0)

    weather = fetch_weather_openmeteo(city, lang)
    if weather:
        print(weather)
        weather = weather.replace(" forecast", "")
        send_notification("Jarvis", f"{weather}")
        sys.exit(0)

    print("Failed to fetch weather", file=sys.stderr)
    sys.exit(1)
