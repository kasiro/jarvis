# Research: Часто используемые команды без wake word

## Дата: 2026-03-09
## Тикет: m3n4o5p6

## Проблема
Часто используемые команды (браузер, погода, калькулятор) требуют wake word что избыточно.

## Решение
Добавить `wake_word_required = false` для часто используемых команд.

## Выполненные изменения

### 1. resources/commands/browser/command.toml
- `browser_open` - wake_word_required: false

### 2. resources/commands/calculator/command.yaml
- `calc_on` - wake_word_required: false
- `calc_off` - wake_word_required: false

### 3. resources/commands/weather/command.toml
- `weather` - wake_word_required: false

## Команды без wake word (итоговый список)

### Критические команды:
- `terminate` (выключись, вырубись, закройся...)

### Часто используемые:
- `browser_open` (открой браузер, запусти браузер...)
- `calc_on` (включи калькулятор, открой калькулятор...)
- `calc_off` (закрой калькулятор, выключи калькулятор...)
- `weather` (какая погода, погода...)

## Тестирование
- ✅ cargo check -p jarvis-core: PASSED
- ✅ TOML парсер читает поле
- ✅ YAML парсер читает поле

## Next Steps
Перейти к тику q7r8s9t0: Документация для разработчиков
