# Jarvis Workspace API PRD

## HR Eng

| Jarvis Workspace API PRD |  | Новая функция Jarvis API для управления рабочими столами и приложениями: запуск приложений на конкретных рабочих столах, переключение между столами, управление окнами. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: AI Assistant **Intended audience**: Engineering | **Status**: Draft **Created**: 2026-03-09 | **Self Link**: `${SESSION_ROOT}/prd.md` **Context**: Jarvis Voice Assistant | 

## Introduction

Функция позволяет Jarvis **управлять рабочими столами** и **приложениями** на них: запускать приложения на конкретных рабочих столах, переключаться между столами, разворачивать/сворачивать окна.

## Problem Statement

**Current Process:** Пользователь должен вручную переключаться между рабочими столами и управлять окнами
**Primary Users:** Пользователи Jarvis на Linux (GNOME/KDE)
**Pain Points:** 
- Нет автоматизации управления рабочими столами
- Приложения запускаются на текущем столе без контроля
- Невозможно быстро переключиться на стол с приложением
- Свёрнутые окна нужно разворачивать вручную

**Importance:** Улучшение UX, автоматизация рутинных действий, интеграция с workspace management

## Objective & Scope

**Objective:** Создать Jarvis API функцию для управления рабочими столами и приложениями
**Ideal Outcome:** Пользователь может голосом управлять рабочими столами и приложениями

### In-scope or Goals
- ✅ Функция `jarvis.workspace.launch_app(app_name, workspace_number)`
- ✅ Функция `jarvis.workspace.switch_to(workspace_number)`
- ✅ Функция `jarvis.workspace.focus_app(app_name)`
- ✅ Поддержка Linux (GNOME/KDE) через wmctrl/xdotool
- ✅ Интеграция в Python Jarvis API
- ✅ Документация и примеры использования

### Not-in-scope or Non-Goals
- ❌ Поддержка Windows (только Linux)
- ❌ Поддержка macOS (только Linux)
- ❌ Создание/удаление рабочих столов
- ❌ Перемещение окон между столами (v2)

## Product Requirements

### Critical User Journeys (CUJs)

1. **CUJ-1: Запуск приложения на рабочем столе 2**
   - Пользователь: "Jarvis, открой браузер на втором рабочем столе"
   - Jarvis: Переключается на workspace 2 → Запускает браузер → Возвращается на workspace 1
   - Ожидание: Приложение запущено на указанном столе

2. **CUJ-2: Переключение на рабочий стол с приложением**
   - Пользователь: "Jarvis, покажи терминал"
   - Jarvis: Ищет терминал → Переключается на его рабочий стол → Разворачивает окно
   - Ожидание: Окно терминала активно и развёрнуто

3. **CUJ-3: Развёртывание свёрнутого приложения**
   - Пользователь: "Jarvis, открой калькулятор"
   - Jarvis: Ищет калькулятор → Если свёрнут → Разворачивает → Переключается на его стол
   - Ожидание: Калькулятор активен и виден

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | `launch_app(app_name, workspace)` | Как пользователь, я хочу запускать приложения на конкретных столах |
| P0 | `switch_to(workspace)` | Как пользователь, я хочу переключаться между столами |
| P0 | `focus_app(app_name)` | Как пользователь, я хочу быстро найти и развернуть приложение |
| P1 | Поддержка GNOME (wmctrl) | Как пользователь GNOME, я хочу чтобы это работало |
| P1 | Поддержка KDE (kwin) | Как пользователь KDE, я хочу чтобы это работало |
| P2 | Интеграция в Python API | Как разработчик команд, я хочу использовать API |

## Assumptions

- Пользователь использует Linux с GNOME или KDE
- Установлены wmctrl и xdotool
- Рабочие столы включены в настройках DE

## Risks & Mitigations

- **Risk:** wmctrl/xdotool не установлены → **Mitigation:** Проверка зависимостей, инструкция по установке
- **Risk:** Разные DE имеют разные API → **Mitigation:** Авто-определение DE, поддержка GNOME/KDE
- **Risk:** Приложения нет в списке окон → **Mitigation:** Запуск приложения если не найдено

## Tradeoff

- **Option 1:** Использовать только wmctrl
  - Pros: Проще, меньше зависимостей
  - Cons: Меньше возможностей
- **Option 2:** wmctrl + xdotool (ВЫБРАНО)
  - Pros: Полный контроль над окнами
  - Cons: Две зависимости

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State | Future State | Impact |
| :---- | :---- | :---- | :---- |
| Автоматизация | 0% | 80% | +80% productivity |
| Поддерживаемые DE | N/A | GNOME, KDE | 2 DE supported |
| Время переключения | ~5 сек (ручное) | ~1 сек (API) | -80% time |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Manager | Оркестрация | Координация |
| User | End User | Feedback | UX testing |
