#!/bin/bash
# Свернуть все окна (Show Desktop)
# Linux: использует dbus для GNOME

# Метод 1: GNOME Show Desktop
dbus-send --session --dest=org.gnome.Shell --type=method_call \
    /org/gnome/Shell org.gnome.Shell.Eval \
    string:"Main.wm.actionShowDesktop()" 2>/dev/null

# Метод 2: xdotool fallback
if command -v xdotool &> /dev/null; then
    xdotool key super+d 2>/dev/null
fi

exit 0
