# Research: Пометить команды стоп/прекрати

## Дата: 2026-03-09
## Тикет: i9j0k1l2

## Проблема
Критические команды (стоп, прекрати, terminate) требуют wake word что замедляет реакцию.

## Решение
Добавить `wake_word_required: false` в файлы команд.

## Выполненные изменения

### 1. resources/commands/terminate/command.yaml
Добавлено поле:
```yaml
command:
    action: terminate
    wake_word_required: false
```

### 2. crates/jarvis-core/src/commands/structs.rs
Добавлено поле в `LegacyCommandData`:
```rust
#[serde(default = "default_true")]
pub wake_word_required: bool,
```

### 3. crates/jarvis-core/src/commands.rs
Обновлено создание `JCommand` из legacy YAML:
```rust
wake_word_required: legacy.command.wake_word_required,
```

## Тестирование
- ✅ cargo check -p jarvis-core: PASSED
- ✅ YAML парсер читает поле
- ✅ Default значение: true (обратная совместимость)

## Команды без wake word
- `terminate` (выключись, вырубись, закройся...) - wake_word_required: false

## Next Steps
Перейти к тику m3n4o5p6: Пометить часто используемые команды
