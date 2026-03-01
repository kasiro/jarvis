#!/bin/bash
# JARVIS Voice Assistant Launcher
# Запуск с правильными переменными окружения для Wayland и Vosk совместимости

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ "$SCRIPT_DIR/resources/commands" -nt "$SCRIPT_DIR/target/release/resources/commands" ]; then
    echo "🥒 Обновление ресурсов..."
    bash "$SCRIPT_DIR/post_build.sh"
fi

# Используем X11 бэкенд для GTK (tray icon)
export GDK_BACKEND=x11

# Отключаем композитинг для WebKit (исправление белого экрана)
export WEBKIT_DISABLE_COMPOSITING_MODE=1

# Устанавливаем C локаль для чисел (исправление Vosk JSON с запятыми)
export LC_NUMERIC=C

# Определяем какую версию запускать
if [ -f "$SCRIPT_DIR/target/release/jarvis-app" ] && [ -d "$SCRIPT_DIR/target/release/resources" ]; then
    # Release сборка (продакшен)
    echo "🥒 Запуск Jarvis (release профиль)..."
    exec "$SCRIPT_DIR/target/release/jarvis-app"
else
    echo "❌ Ошибка: jarvis-app не найден!"
    echo ""
    echo "Сначала соберите проект:"
    echo "  ./rebuild.sh        # для release сборки"
    exit 1
fi
