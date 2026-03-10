# Research: wake_word_required поле в JCommand

## Дата: 2026-03-09
## Тикет: a1b2c3d4

## Проблема
Структура команды в Rust не поддерживает поле для указания необходимости wake word фразы.

## Решение
Добавить поле `wake_word_required: bool` в структуру `JCommand`.

## Изменения

### 1. crates/jarvis-core/src/commands/structs.rs

**Добавлено:**
- Helper функция `default_true()` возвращает `true`
- Поле `wake_word_required: bool` с `#[serde(default = "default_true")]`
- Default значение: `true` (обратная совместимость)
- Обновлены `Default` и `Clone` impl

### 2. crates/jarvis-core/src/commands.rs

**Обновлено:**
- Создание `JCommand` для legacy YAML команд включает `wake_word_required: true`

## Обратная совместимость
- Поле имеет default значение `true`
- Старые команды без поля будут требовать wake word
- TOML/YAML могут явно указать `wake_word_required = false`

## Тестирование
- ✅ cargo check -p jarvis-core: PASSED
- ✅ Компиляция без ошибок

## Следующий шаг
Изменить STT/распознавание для проверки поля `wake_word_required` (тикет e5f6g7h8)
