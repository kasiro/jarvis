# Исправление legacy YAML - алиас cli_path → cli_cmd

## Overview
Добавить serde алиас для поля `cli_cmd` в структуре `LegacyCommandData` чтобы поддержать legacy YAML формат с `cli_path`.

## Scope Definition (CRITICAL)
### In Scope
- Добавить `#[serde(alias = "cli_path")]` к полю `cli_cmd`
- Собрать проект
- Проверить команду "запусти диспетчер задач"

### Out of Scope (DO NOT TOUCH)
- Изменение других полей структуры
- Рефакторинг парсера команд
- Изменение TOML формата

## Current State Analysis
- Файл: `crates/jarvis-core/src/commands/structs.rs`
- Строки 25-35: `LegacyCommandData` структура
- Поле `cli_cmd: String` без алиаса
- YAML использует `cli_path`, парсер ожидает `cli_cmd` → пустая команда

## Implementation Phases

### Phase 1: Исправление структуры
- **Goal**: Добавить алиас `cli_path` к `cli_cmd`
- **Steps**:
  1. [ ] Открыть `crates/jarvis-core/src/commands/structs.rs`
  2. [ ] Изменить строку 32: `#[serde(alias = "cli_path", default)]` для `pub cli_cmd: String`
  3. [ ] Сохранить файл
- **Verification**: `cargo check --workspace` без ошибок

### Phase 2: Сборка и тестирование
- **Goal**: Собрать проект и проверить команду
- **Steps**:
  1. [ ] Запустить `./rebuild.sh --fast`
  2. [ ] Запустить Jarvis: `./jarvis.sh`
  3. [ ] Произнести "джарвис запусти диспетчер задач"
  4. [ ] Проверить логи - команда должна выполниться
- **Verification**: Диспетчер задач открывается, в логах `Spawning: sh -c /path/to/script.sh []`

## Success Criteria
1. ✅ `cargo check --workspace` проходит
2. ✅ Сборка успешна
3. ✅ Команда "запусти диспетчер задач" работает
