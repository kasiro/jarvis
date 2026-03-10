# Research: STT проверка wake_word_required

## Дата: 2026-03-09
## Тикет: e5f6g7h8

## Проблема
STT модуль не проверяет поле `wake_word_required` перед выполнением команды.
Все команды требуют wake word фразы.

## Архитектура
1. **app.rs** - основной цикл:
   - `'wake_word: loop` - ждёт wake word
   - `recognize_command()` - распознаёт команду после wake word
   - `execute_command()` - выполняет команду

2. **commands.rs**:
   - `fetch_command()` - ищет команду по фразе (fuzzy match)
   - `execute_command()` - выполняет команду

## Решение
Добавить **отдельный поток** для команд без wake word:

### Вариант 1: Параллельная проверка
- Перед основным циклом wake word проверять фразу на команды без wake word
- Если найдена команда с `wake_word_required: false` - выполнить немедленно

### Вариант 2: Фильтрация в fetch_command
- Добавить параметр `require_wake_word: Option<bool>` в `fetch_command`
- Фильтровать команды по полю `wake_word_required`

**ВЫБРАНО: Вариант 1** - более явный и производительный

## План изменений

### 1. crates/jarvis-core/src/commands.rs
- Добавить функцию `fetch_command_no_wake_word()` 
- Ищет только команды с `wake_word_required: false`

### 2. crates/jarvis-app/src/app.rs
- В начале `recognize_command()` проверить команды без wake word
- Если найдена - выполнить немедленно
- Иначе продолжить обычный цикл

## Тестирование
- Команда с `wake_word_required: false` выполняется без wake word
- Команда с `wake_word_required: true` требует wake word
