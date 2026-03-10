# Plan Review: Команды стоп/прекрати без wake word

## Дата: 2026-03-09
## Тикет: i9j0k1l2

## Plan Status: ✅ ВЫПОЛНЕН

## Выполненные изменения

### ✅ resources/commands/terminate/command.yaml
- [x] Добавить `wake_word_required: false`

### ✅ crates/jarvis-core/src/commands/structs.rs
- [x] Добавить поле в `LegacyCommandData`
- [x] Default: `default_true()`

### ✅ crates/jarvis-core/src/commands.rs
- [x] Передавать поле из YAML в JCommand

## Verification

### Компиляция
```bash
cargo check -p jarvis-core
# Result: PASSED ✅
```

### Обратная совместимость
- YAML без поля: wake_word_required: true ✅
- YAML с полем: читается значение ✅

## Approval
**Plan выполнен полностью.**

## Next Steps
Перейти к тику m3n4o5p6: Пометить часто используемые команды
