---
id: LINUX_PORT_EPIC
title: '[Epic] Перенос JARVIS на Linux CachyOS GNOME Wayland'
status: Todo
priority: High
order: 0
created: '2026-02-22'
updated: '2026-02-22'
links:
  - url: ./conductor/product.md
    title: PRD Документ
---

# Description

## Problem to solve
Проект JARVIS написан исключительно для Windows и использует множество Windows-специфичных технологий: AutoHotkey скрипты, WinRT API, PowerShell/cmd вызовы, winapi зависимости. Проект не собирается и не работает на Linux.

## Solution
Полная адаптация проекта для Linux CachyOS с GNOME Wayland через:
- Замену AHK скриптов на bash + xdotool/wmctrl
- Адаптацию системных API (clipboard, notifications, file explorer)
- Удаление Windows-specific зависимостей
- Исправление platform-specific условий компиляции

## Implementation Details
- 21 AutoHotkey скрипт требуют замены
- 9 файлов Rust кода требуют изменений
- 5 конфигурационных файлов требуют обновлений
- Требуется тестирование на CachyOS GNOME Wayland
- Критический приоритет - функциональный паритет

## Child Tickets
Смотрите дочерние тикеты в директории `./ .pickle_sessions/2026-02-22-2adc8d16/`
