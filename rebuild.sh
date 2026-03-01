#!/bin/bash

# Pickle Rick's Jarvis Rebuild Script 🥒
# Builds all Jarvis components and copies resources

set -e

echo "🥒 Pickle Rick's Jarvis Rebuild Script"
echo "======================================"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    echo -e "${YELLOW}>>>${NC} $1"
}

print_success() {
    echo -e "${GREEN}>>>${NC} $1"
}

print_error() {
    echo -e "${RED}>>>${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}>>>${NC} $1"
}

# Parse arguments
CLEAN_BUILD=false
USE_RUSTPOTTER=false
BUILD_APP_ONLY=false
BUILD_GUI=false  # GUI собирается только при явном указании --gui
TAURI_TIMEOUT=600  # 10 минут на сборку Tauri

for arg in "$@"; do
    case $arg in
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --skip-gui)
            print_warning "--skip-gui устарел: GUI теперь не собирается по умолчанию"
            shift
            ;;
        --rustpotter)
            USE_RUSTPOTTER=true
            shift
            ;;
        --app)
            BUILD_APP_ONLY=true
            shift
            ;;
        --gui)
            BUILD_GUI=true
            shift
            ;;
        --help)
            echo "Использование: $0 [OPTIONS]"
            echo ""
            echo "OPTIONS:"
            echo "  --clean        Очистить перед сборкой"
            echo "  --skip-gui     Устарел (GUI не собирается по умолчанию)"
            echo "  --rustpotter   Собрать с RustPotter wake-word"
            echo "  --app          Собрать только jarvis-app (автоматически включает core)"
            echo "  --gui          Собрать jarvis-app + jarvis-gui (Tauri)"
            echo "  --help         Показать эту справку"
            echo ""
            echo "EXAMPLES:"
            echo "  ./rebuild.sh --app              # Только app + core"
            echo "  ./rebuild.sh --gui              # App + GUI"
            echo "  ./rebuild.sh                    # Только app (GUI не собирается)"
            echo ""
            exit 0
            ;;
    esac
done

# Step 0: Check for required system libraries
print_status "Checking system dependencies..."

check_library() {
    local lib=$1
    local package=$2
    if ! ldconfig -p | grep -q "$lib" 2>/dev/null; then
        print_warning "Библиотека $lib не найдена. Установите: $package"
        return 1
    fi
    return 0
}

MISSING_LIBS=0

# Check for libxdo (required by libxdo-sys)
check_library "libxdo.so" "libxdo-dev" || MISSING_LIBS=1

# Check for libvosk (required by vosk-sys)
check_library "libvosk.so" "libvosk-dev" || MISSING_LIBS=1

# Check for libasound (required by cpal/alsa)
check_library "libasound.so" "libasound2-dev" || MISSING_LIBS=1

# Check for Lua 5.4 (required by mlua with lua54 feature)
if ! ldconfig -p | grep -q "liblua.so.5.4" 2>/dev/null; then
    print_warning "Библиотека Lua 5.4 не найдена. Установите: lua (Arch) или liblua5.4-dev (Debian/Ubuntu)"
    MISSING_LIBS=1
fi

# RustPotter - это Rust крейт, не требует системной библиотеки!
# Проверка удалена - компилируется вместе с проектом

if [ $MISSING_LIBS -eq 1 ]; then
    echo ""
    print_warning "Обнаружены недостающие библиотеки!"
    
    # Проверка LIBRARY_PATH
    if [ -n "$LIBRARY_PATH" ]; then
        print_status "Текущий LIBRARY_PATH: $LIBRARY_PATH"
    else
        print_warning "LIBRARY_PATH не установлен!"
        print_status "Возможно библиотеки установлены, но не в стандартных путях"
        print_status "Проверьте:"
        print_status "  find /usr -name 'libvosk.so' 2>/dev/null"
        print_status "  find /usr/local -name 'libxdo.so' 2>/dev/null"
    fi
    
    print_error "Сборка отменена!"
    print_status "Установите недостающие библиотеки:"
    echo ""
    echo "  # Debian/Ubuntu:"
    echo "  sudo apt install libxdo-dev libvosk-dev libasound2-dev liblua5.4-dev"
    echo ""
    echo "  # Fedora/RHEL:"
    echo "  sudo dnf install libxdo-devel vosk-devel alsa-devel lua-devel"
    echo ""
    echo "  # Arch Linux:"
    echo "  sudo pacman -S xdotool vosk alsa-lib lua"
    echo ""
    exit 1
fi

print_success "Проверка завершена"
echo ""

# Step 1: Set environment variables
print_status "Настройка переменных окружения..."

# Автоматическая установка LIBRARY_PATH если пустая
if [ -z "$LIBRARY_PATH" ]; then
    print_status "LIBRARY_PATH не установлен, устанавливаем..."
    export LIBRARY_PATH="/usr/lib:/usr/local/lib"
else
    print_status "Добавляем стандартные пути в LIBRARY_PATH..."
    export LIBRARY_PATH="/usr/lib:/usr/local/lib:$LIBRARY_PATH"
fi

# PKG_CONFIG_PATH
if [ -z "$PKG_CONFIG_PATH" ]; then
    export PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/local/lib/pkgconfig"
else
    export PKG_CONFIG_PATH="/usr/lib/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
fi

export CARGO_BUILD_JOBS="4"
print_success "Переменные установлены"
echo ""

# Step 2: Clean build (if requested)
if [ "$CLEAN_BUILD" = true ]; then
    print_status "Очистка предыдущих артефактов сборки..."
    cargo clean
    print_success "Очистка завершена"
    echo ""
elif [ "$USE_RUSTPOTTER" = true ]; then
    # Автоматическая очистка при --rustpotter (НО только в начале!)
    print_status "Флаг --rustpotter обнаружен!"
    print_status "Автоматическая очистка для переключения на RustPotter..."
    cargo clean
    print_success "Очистка завершена"
    echo ""
else
    print_status "Подготовка к сборке (incremental)..."
    print_warning "Для чистой сборки используйте: ./rebuild.sh --clean"
    print_success "Готово"
    echo ""
fi

# Step 3: Build based on flags

# Generate build version string for logging
BUILD_VERSION="jarvis-$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
print_info "Build version: $BUILD_VERSION"

# Export BUILD_VERSION for cargo to embed in binary
export BUILD_VERSION

echo ""

if [ "$BUILD_GUI_ONLY" = true ]; then
    # Только GUI (устаревший режим, оставлен для совместимости)
    print_warning "Режим --gui-only устарел, используйте --gui для app+gui"
    print_status "Сборка jarvis-gui (Tauri)..."
    if command -v cargo-tauri &> /dev/null; then
        print_info "Запуск cargo tauri build..."
        if timeout "$TAURI_TIMEOUT" cargo tauri build --verbose 2>&1; then
            print_success "jarvis-gui собран"
        else
            EXIT_CODE=$?
            if [ $EXIT_CODE -eq 124 ]; then
                print_error "Сборка GUI превысила таймаут (${TAURI_TIMEOUT}s)!"
            else
                print_error "Ошибка сборки GUI (код: $EXIT_CODE)"
            fi
        fi
    else
        print_warning "cargo-tauri не установлен. Пропускаем..."
    fi
elif [ "$BUILD_APP_ONLY" = true ]; then
    # Только app (автоматически собирает core)
    print_status "Сборка jarvis-app (включает jarvis-core)..."
    if [ "$USE_RUSTPOTTER" = true ]; then
        cargo build --release -p jarvis-app --features jarvis-core/rustpotter_wake
        print_success "jarvis-app собран (release + rustpotter)"
    else
        cargo build --release -p jarvis-app
        print_success "jarvis-app собран"
    fi
    echo ""

    # Копирование ресурсов
    print_status "Запуск post_build.sh..."
    bash "$SCRIPT_DIR/post_build.sh"
    print_success "Ресурсы скопированы в target/release/"
    echo ""

    # Summary
    echo "======================================"
    print_success "🥒 Сборка завершена!"
    echo ""
    echo "Расположение бинарников (release):"
    echo "  - target/release/jarvis-app"
    echo ""
    echo "Расположение ресурсов:"
    echo "  - target/release/resources/"
    echo ""
    echo "Для запуска Jarvis:"
    echo "  ./target/release/jarvis-app"
    echo "======================================"
    exit 0
else
    # Полная сборка всех компонентов

    # Step 1: jarvis-app (автоматически собирает jarvis-core)
    print_status "Сборка jarvis-app (включает jarvis-core)..."
    if [ "$USE_RUSTPOTTER" = true ]; then
        cargo build --release -p jarvis-app --features jarvis-core/rustpotter_wake
        print_success "jarvis-app собран (release + rustpotter)"
    else
        cargo build --release -p jarvis-app
        print_success "jarvis-app собран"
    fi
    echo ""

    # Step 2: jarvis-gui (Tauri) - ТОЛЬКО если указан флаг --gui
    if [ "$BUILD_GUI" = true ]; then
        print_status "Сборка jarvis-gui (Tauri)..."

        # Проверяем путь к GUI бинарнику
        GUI_BIN_PATH="$SCRIPT_DIR/src-tauri/target/release/jarvis-gui"

        if [ -f "$GUI_BIN_PATH" ]; then
            print_info "GUI бинарник уже существует: $GUI_BIN_PATH"
            print_warning "Пропускаем сборку GUI (уже собран)"
        else
            if command -v cargo-tauri &> /dev/null; then
                print_info "Запуск cargo tauri build (таймаут: ${TAURI_TIMEOUT}s)..."

                if timeout "$TAURI_TIMEOUT" cargo tauri build --verbose 2>&1; then
                    print_success "jarvis-gui собран"
                else
                    EXIT_CODE=$?
                    if [ $EXIT_CODE -eq 124 ]; then
                        print_error "Сборка GUI превысила таймаут (${TAURI_TIMEOUT}s)!"
                        print_warning "GUI не собран, но остальные компоненты готовы"
                    else
                        print_error "Ошибка сборки GUI (код: $EXIT_CODE)"
                    fi
                fi
            else
                print_warning "cargo-tauri не установлен. Пропускаем jarvis-gui..."
                print_status "Для установки: cargo install tauri-cli"
            fi
        fi
    else
        print_warning "GUI не собирается (используйте --gui для сборки app+gui)"
    fi
    echo ""

    # Step 3: post_build
    print_status "Запуск post_build.sh..."
    bash "$SCRIPT_DIR/post_build.sh"
    print_success "Ресурсы скопированы в target/release/"
    echo ""

    # Summary
    echo "======================================"
    print_success "🥒 Пересборка завершена, Morty!"
    echo ""
    echo "Расположение бинарников (release):"
    echo "  - target/release/jarvis-app"
    if [ "$USE_RUSTPOTTER" = true ]; then
        echo ""
        echo "🥒 RustPotter wake-word ВКЛЮЧЁН!"
        echo "   Для использования настройте в ~/.config/com.priler.jarvis/app.db:"
        echo "   wake_word_engine = \"rustpotter\""
    fi
    if [ "$BUILD_GUI" = true ] && command -v cargo-tauri &> /dev/null; then
        echo "  - src-tauri/target/release/jarvis-gui"
    fi
    echo ""
    echo "Расположение ресурсов:"
    echo "  - target/release/resources/"
    echo ""
    echo "Для запуска Jarvis:"
    echo "  ./target/release/jarvis-app"
    echo "======================================"
fi
