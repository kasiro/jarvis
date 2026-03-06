#!/bin/bash
# JARVIS Voice Assistant Launcher
# Запуск с правильными переменными окружения для Wayland и Vosk совместимости

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Используем X11 бэкенд для GTK (tray icon)
export GDK_BACKEND=x11

# Отключаем композитинг для WebKit (исправление белого экрана)
export WEBKIT_DISABLE_COMPOSITING_MODE=1

# Устанавливаем C локаль для чисел (исправление Vosk JSON с запятыми)
export LC_NUMERIC=C

# Определяем какую версию запускать (приоритет: release > fast > debug)
if [ -f "$SCRIPT_DIR/target/release/jarvis-app" ] && [ -d "$SCRIPT_DIR/target/release/resources" ]; then
    # Release сборка (продакшен)
    echo "🥒 Запуск Jarvis (release профиль)..."
    exec "$SCRIPT_DIR/target/release/jarvis-app"
elif [ -f "$SCRIPT_DIR/target/fast/jarvis-app" ] && [ -d "$SCRIPT_DIR/target/fast/resources" ]; then
    # Fast сборка (быстрая dev)
    echo "🥒 Запуск Jarvis (fast профиль)..."
    exec "$SCRIPT_DIR/target/fast/jarvis-app"
elif [ -f "$SCRIPT_DIR/target/debug/jarvis-app" ] && [ -d "$SCRIPT_DIR/target/debug/resources" ]; then
    # Debug/Dev сборка (отладка)
    echo "🥒 Запуск Jarvis (dev/debug профиль)..."
    exec "$SCRIPT_DIR/target/debug/jarvis-app"
else
    echo "❌ Ошибка: jarvis-app не найден!"
    echo ""
    echo "Сначала соберите проект:"
    echo "  ./rebuild.sh        # release сборка (по умолчанию)"
    echo "  ./rebuild.sh --dev  # dev сборка (быстрая отладка)"
    echo "  ./rebuild.sh --fast # fast сборка (легкие оптимизации)"
    exit 1
fi
