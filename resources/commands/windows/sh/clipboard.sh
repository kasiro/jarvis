#!/bin/bash
# Буфер обмена
# Linux: показываем содержимое буфера

# Метод 1: wl-paste (Wayland)
if command -v wl-paste &> /dev/null; then
    wl-paste
    exit 0
fi

# Метод 2: xclip (X11)
if command -v xclip &> /dev/null; then
    xclip -selection clipboard -o
    exit 0
fi

# Метод 3: xsel
if command -v xsel &> /dev/null; then
    xsel --clipboard --output
    exit 0
fi

echo "Error: No clipboard tool found"
echo "Install: wl-clipboard, xclip, or xsel"
exit 1
