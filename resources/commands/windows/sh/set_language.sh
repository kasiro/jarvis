#!/bin/bash
# Смена раскладки клавиатуры
# Linux: переключение на следующую раскладку

# Метод 1: gsettings (GNOME)
if command -v gsettings &> /dev/null; then
    # Эмуляция нажатия Super+Space (переключение раскладки)
    if command -v xdotool &> /dev/null; then
        xdotool key super+space
        exit 0
    fi
fi

# Метод 2: setxkbmap (принудительная установка)
if command -v setxkbmap &> /dev/null; then
    # Переключение между ru и en
    current=$(setxkbmap -query | grep layout | awk '{print $2}')
    if [ "$current" = "us" ]; then
        setxkbmap ru
    else
        setxkbmap us
    fi
    exit 0
fi

echo "Error: Cannot change keyboard layout"
exit 1
