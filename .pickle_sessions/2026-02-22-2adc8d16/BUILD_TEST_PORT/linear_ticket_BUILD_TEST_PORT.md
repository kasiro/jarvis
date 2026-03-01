---
id: BUILD_TEST_PORT
title: 'Тестирование сборки и запуска на CachyOS'
status: Todo
priority: High
order: 80
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ../linear_ticket_LINUX_PORT_EPIC.md
    title: Parent Ticket
---

# Description

## Problem to solve
После всех изменений необходимо убедиться что проект:
- Собирается без ошибок на Linux
- Запускается и работает корректно
- Все голосовые команды выполняются

## Solution
Провести полное тестирование сборки и функциональности на CachyOS GNOME Wayland.

## Implementation Details
### Шаг 1: Установка зависимостей
```bash
# Системные пакеты Arch/CachyOS
sudo pacman -S xdotool wmctrl xclip libnotify gnome-screenshot
sudo pacman -S libappindicator-gtk3 libgtk-3-dev

# Rust зависимости
cargo install --force cargo-audit
```

### Шаг 2: Сборка проекта
```bash
# Проверка
cargo check

# Сборка
cargo tauri build

# Или для разработки
cargo tauri dev
```

### Шаг 3: Функциональное тестирование
1. **Запуск приложения** - проверить что GUI открывается
2. **Tray icon** - проверить отображение в GNOME tray
3. **Голосовое управление** - проверить wake word detection
4. **Команды:**
   - Открытие браузера
   - Управление окнами
   - Скриншоты
   - Буфер обмена
   - Уведомления
   - Управление звуком

### Шаг 4: Исправление ошибок
- Задокументировать все найденные ошибки
- Исправить проблемы с Wayland совместимостью
- Проверить права доступа для системных вызовов

### Критерии успеха:
- `cargo build` проходит без ошибок
- Приложение запускается без паник
- 21/21 команда работают корректно
- Уведомления отображаются
- Буфер обмена работает
