# Jarvis Multi-Agent Audit PRD

## HR Eng

| Jarvis Multi-Agent Audit PRD |  | Комплексный аудит проекта Jarvis с использованием 4 параллельных агентов для проверки wake_word_required протокола, тестирования команд, документации и производительности. |
| :---- | :---- | :---- |
| **Author**: Pickle Rick **Contributors**: 4 Morty Agents **Intended audience**: Engineering | **Status**: Draft **Created**: 2026-03-09 | **Self Link**: `${SESSION_ROOT}/prd.md` **Context**: Jarvis Voice Assistant | 

## Introduction

После исправления wake_word_required протокола требуется **комплексная проверка** всех компонентов системы. 4 агента работают **параллельно** для полного аудита проекта.

## Problem Statement

**Current Process:** Ручная проверка команд, документации и тестов
**Primary Users:** Разработчики Jarvis, пользователи голосового ассистента
**Pain Points:** 
- Ручная проверка всех команд занимает время
- Возможны нарушения протокола wake_word_required
- Недостаточное тестирование
- Документация устарела
- Производительность VAD/STT не оптимизирована

**Importance:** Обеспечить качество, безопасность и производительность системы

## Objective & Scope

**Objective:** Автоматизированный аудит проекта 4 независимыми агентами
**Ideal Outcome:** Полный отчёт о состоянии проекта с рекомендациями

### In-scope or Goals
- ✅ Аудит всех команд на соответствие протоколу wake_word_required
- ✅ Тестирование команд без wake word
- ✅ Обновление документации
- ✅ Анализ производительности VAD/STT

### Not-in-scope or Non-Goals
- ❌ Изменение архитектуры Jarvis
- ❌ Добавление новых функций
- ❌ Рефакторинг кода (только рекомендации)

## Product Requirements

### Critical User Journeys (CUJs)

1. **CUJ-1: Code Audit Agent**
   - Сканирует `resources/commands/**/*.{toml,yaml}`
   - Проверяет наличие `wake_word_required`
   - Составляет отчёт о нарушениях
   - Предлагает исправления

2. **CUJ-2: Testing Agent**
   - Запускает тестовые команды
   - Проверяет работу без wake word
   - Проверяет что voice команды требуют wake word
   - Составляет отчёт о результатах

3. **CUJ-3: Documentation Agent**
   - Обновляет `FIX.md`
   - Обновляет `ADD.md`
   - Создаёт `WAKE_WORD_PROTOCOL.md`
   - Добавляет примеры

4. **CUJ-4: Performance Agent**
   - Анализирует логи VAD/STT
   - Измеряет задержки
   - Предлагает оптимальные настройки
   - Проверяет на ложные срабатывания

### Functional Requirements

| Priority | Requirement | User Story |
| :---- | :---- | :---- |
| P0 | Code Audit Agent | Как разработчик, я хочу знать какие команды нарушают протокол |
| P0 | Testing Agent | Как пользователь, я хочу чтобы команды работали корректно |
| P1 | Documentation Agent | Как разработчик, я хочу актуальную документацию |
| P1 | Performance Agent | Как пользователь, я хочу минимальные задержки |

## Assumptions

- Агенты работают независимо и параллельно
- Каждый агент создаёт полную документацию (research, plan, review)
- Результаты агентов будут валидированы перед завершением

## Risks & Mitigations

- **Risk:** Агенты работают слишком долго → **Mitigation:** Timeout 600-900s на агента
- **Risk:** Агенты не справляются с задачей → **Mitigation:** Валидация результатов менеджером
- **Risk:** Конфликты между агентами → **Mitigation:** Изолированные директории для каждого

## Tradeoff

- **Option 1:** Последовательный запуск агентов
  - Pros: Проще контролировать
  - Cons: Долго (4x время)
- **Option 2:** Параллельный запуск (ВЫБРАНО)
  - Pros: Быстро, эффективно
  - Cons: Требует координации

## Business Benefits/Impact/Metrics

**Success Metrics:**

| Metric | Current State | Future State | Impact |
| :---- | :---- | :---- | :---- |
| Нарушения протокола | Неизвестно | 0 | 100% compliance |
| Задержка команд | ~0.8-1.0с | ~0.5-0.8с | -40% latency |
| Документация | Устарела | Актуальна | +100% coverage |
| Тесты | Отсутствуют | Есть | +100% coverage |

## Stakeholders / Owners

| Name | Team/Org | Role | Note |
| :---- | :---- | :---- | :---- |
| Pickle Rick | Manager | Оркестрация | Координация агентов |
| Code Audit Morty | Worker | Аудит кода | Проверка протокола |
| Testing Morty | Worker | Тестирование | Проверка команд |
| Docs Morty | Worker | Документация | Обновление docs |
| Performance Morty | Worker | Производительность | Оптимизация VAD/STT |
