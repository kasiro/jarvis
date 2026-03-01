#!/bin/bash
# JARVIS Command Template
# Описание: Шаблон для bash скриптов команд JARVIS
# Использование: ./template.sh

set -e

# Логирование
log() {
    echo "[INFO] $1" >&2
}

error() {
    echo "[ERROR] $1" >&2
}

# Проверка зависимостей
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        error "$1 not found. Please install: $2"
        exit 1
    fi
}

# Основная логика команды
main() {
    log "Command started"
    
    # Ваш код здесь
    echo "Command executed successfully"
    
    log "Command completed"
}

# Запуск
main "$@"
