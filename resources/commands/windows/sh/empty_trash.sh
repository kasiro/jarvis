#!/bin/bash
# Очистка корзины
# Linux: очистка ~/.local/share/Trash

# Очистка через dbus (GNOME Files/Nautilus)
dbus-send --session --dest=org.gnome.Nautilus.TrashMonitor \
    /org/gnome/Nautilus/TrashMonitor org.gnome.Nautilus.TrashMonitor.Empty \
    2>/dev/null

# Прямое удаление файлов
rm -rf ~/.local/share/Trash/files/* 2>/dev/null
rm -rf ~/.local/share/Trash/info/* 2>/dev/null

exit 0
