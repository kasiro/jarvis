#!/bin/bash
# Скриншот экрана
# Linux: gnome-screenshot или flameshot

SCREENSHOT_DIR="$HOME/Pictures/Screenshots"
mkdir -p "$SCREENSHOT_DIR"
FILENAME="screenshot_$(date +%Y%m%d_%H%M%S).png"

# Метод 1: gnome-screenshot
if command -v gnome-screenshot &> /dev/null; then
    gnome-screenshot -f "$SCREENSHOT_DIR/$FILENAME"
    echo "Screenshot: $SCREENSHOT_DIR/$FILENAME"
    exit 0
fi

# Метод 2: flameshot
if command -v flameshot &> /dev/null; then
    flameshot gui -p "$SCREENSHOT_DIR"
    exit 0
fi

# Метод 3: grim (для Wayland)
if command -v grim &> /dev/null; then
    grim "$SCREENSHOT_DIR/$FILENAME"
    echo "Screenshot: $SCREENSHOT_DIR/$FILENAME"
    exit 0
fi

echo "Error: No screenshot tool found"
echo "Install: gnome-screenshot, flameshot, or grim"
exit 1
