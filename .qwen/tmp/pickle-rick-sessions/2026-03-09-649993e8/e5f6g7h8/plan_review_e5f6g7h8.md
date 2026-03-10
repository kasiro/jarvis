# Plan Review: STT проверка wake_word_required

## Дата: 2026-03-09
## Тикет: e5f6g7h8

## Plan Status: ✅ ВЫПОЛНЕН

## Выполненные изменения

### ✅ crates/jarvis-core/src/commands.rs
- [x] Добавить функцию `fetch_command_no_wake_word()`
- [x] Рефакторинг `fetch_command()` → `fetch_command_internal()`
- [x] Фильтрация команд по полю `wake_word_required`

### ✅ crates/jarvis-app/src/app.rs
- [x] Проверка команд без wake word в начале `recognize_command()`
- [x] Немедленное выполнение если найдена команда без wake word
- [x] Early return после выполнения

## Verification

### Компиляция
```bash
cargo check -p jarvis-core -p jarvis-app
# Result: PASSED ✅
```

### Логика
- `fetch_command()` - все команды (wake_word_required: any)
- `fetch_command_no_wake_word()` - только команды с wake_word_required: false

## Approval
**Plan выполнен полностью.** Код готов к интеграции.

## Next Steps
Перейти к тику i9j0k1l2: Пометить команды стоп/прекрати как wake_word_required: false
