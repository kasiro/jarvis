---
id: fix_cli_yaml_alias
title: Исправить парсинг legacy YAML - добавить алиас cli_path → cli_cmd
status: Todo
priority: High
order: 10
created: 2026-02-24
updated: 2026-02-24
links:
  - url: ../prd.md
    title: PRD
---

# Description

## Problem to solve
Legacy YAML формат команд использует `cli_path`, но структура `LegacyCommandData` ожидает `cli_cmd`. Это приводит к пустой команде при выполнении CLI команд (`sh -c []`).

## Solution
Добавить serde алиас `#[serde(alias = "cli_path")]` для поля `cli_cmd` в структуре `LegacyCommandData`.

## Implementation Details
- Файл: `crates/jarvis-core/src/commands/structs.rs`
- Структура: `LegacyCommandData`
- Изменить поле `cli_cmd` с добавлением алиаса
- Протестировать с существующими YAML файлами команд
- Собрать проект: `./rebuild.sh --fast`
- Проверить команду "запусти диспетчер задач"
