# Plan Review: Часто используемые команды без wake word

## Дата: 2026-03-09
## Тикет: m3n4o5p6

## Plan Status: ✅ ВЫПОЛНЕН

## Выполненные изменения

### ✅ resources/commands/browser/command.toml
- [x] `browser_open` - wake_word_required: false

### ✅ resources/commands/calculator/command.yaml
- [x] `calc_on` - wake_word_required: false
- [x] `calc_off` - wake_word_required: false

### ✅ resources/commands/weather/command.toml
- [x] `weather` - wake_word_required: false

## Verification

### Компиляция
```bash
cargo check -p jarvis-core
# Result: PASSED ✅
```

## Approval
**Plan выполнен полностью.**

## Next Steps
Перейти к тику q7r8s9t0: Документация для разработчиков
