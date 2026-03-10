# Research Docs: Wake Word Protocol Documentation

**Дата:** 2026-03-09  
**Автор:** Documentation Morty  
**Задача:** Обновление документации проекта и создание WAKE_WORD_PROTOCOL.md

---

## 📋 Обзор задачи

### Цель
Создать полную документацию по использованию `wake_word_required` в командах Jarvis.

### Проблема
Отсутствовала стандартизированная документация которая объясняет:
- Что такое `wake_word_required`
- Какие команды МОГУТ иметь `wake_word_required: false`
- Какие команды НЕ МОГУТ иметь `wake_word_required: false`
- Примеры правильной пометки
- Примеры нарушений

---

## 🔍 Исследование

### Проанализированные файлы

#### 1. Конфигурации команд

**TOML команды:**
- `/home/kasiro/Документы/jarvis/resources/commands/browser/command.toml`
- `/home/kasiro/Документы/jarvis/resources/commands/weather/command.toml`
- `/home/kasiro/Документы/jarvis/resources/commands/counter/command.toml`
- `/home/kasiro/Документы/jarvis/resources/commands/test_slots/command.toml`

**YAML команды:**
- `/home/kasiro/Документы/jarvis/resources/commands/terminate/command.yaml`
- `/home/kasiro/Документы/jarvis/resources/commands/calculator/command.yaml`
- `/home/kasiro/Документы/jarvis/resources/commands/jarvis/command.yaml`
- `/home/kasiro/Документы/jarvis/resources/commands/steam/command.yaml`
- `/home/kasiro/Документы/jarvis/resources/commands/windows/command.yaml`
- `/home/kasiro/Документы/jарвис/resources/commands/modes/command.yaml`

#### 2. Исходный код

**Rust код:**
- `/home/kasiro/Документы/jarvis/crates/jarvis-core/src/commands/structs.rs`
  - Структура `JCommand` с полем `wake_word_required: bool`
  - Значение по умолчанию: `true` (через функцию `default_true()`)
  - Legacy формат: `LegacyCommandData` с полем `wake_word_required`

- `/home/kasiro/Документы/jarvis/crates/jarvis-core/src/commands.rs`
  - `fetch_command_no_wake_word()` - поиск команд без wake word
  - `fetch_command_internal()` - внутренняя реализация с фильтром по `wake_word_required`

- `/home/kasiro/Документы/jarvis/crates/jarvis-app/src/app.rs`
  - Интеграция в STT цикл через `recognize_command()`

#### 3. Существующая документация

- `/home/kasiro/Документы/jarvis/resources/commands/WAKE_WORD.md`
  - Базовая документация по командам без wake word
  - Примеры TOML/YAML синтаксиса
  - Общие рекомендации

- `/home/kasiro/Документы/jarvis/ADD.md`
  - Раздел "Команды без Wake Word"
  - Список реализованных функций

- `/home/kasiro/Документы/jarvis/FIX.md`
  - Список проблем для исправления

---

## 📊 Анализ текущих команд

### Команды с `wake_word_required: false`

| Команда | Файл | Тип | Обоснование |
|---------|------|-----|-------------|
| `terminate` | `terminate/command.yaml` | terminate | ✅ Критическая безопасность |
| `browser_open` | `browser/command.toml` | python | ✅ Частое использование |
| `open_ide` | `browser/command.toml` | python | ✅ Частое использование |
| `calc_on` | `calculator/command.yaml` | python | ✅ Частое использование |
| `calc_off` | `calculator/command.yaml` | python | ✅ Частое использование |
| `weather` | `weather/command.toml` | python | ✅ Частое использование |

### Команды с `wake_word_required: true` (по умолчанию)

| Команда | Файл | Тип | Обоснование |
|---------|------|-----|-------------|
| `browser_close` | `browser/command.toml` | python | ✅ Не требует частого использования |
| `close_ide` | `browser/command.toml` | python | ✅ Не требует частого использования |
| `open_web_search` | `browser/command.toml` | cli | ✅ Альтернатива browser_open |
| `counter` | `counter/command.toml` | lua | ✅ Специфичная команда |
| `set_city` | `weather/command.toml` | lua | ✅ Редкое использование |
| Voice команды | `jarvis/command.yaml` | voice | ✅ Развлечения |
| Режимы | `modes/command.yaml` | python | ✅ Переключение режимов |
| Windows команды | `windows/command.yaml` | ahk/cli | ✅ Системные действия |
| Steam команды | `steam/command.yaml` | ahk | ✅ Игровые сессии |

---

## 🎯 Классификация команд

### Категория 1: Критические команды безопасности

**Характеристики:**
- Должны работать ВСЕГДА
- Экстренные ситуации
- Остановка системы

**Команды:**
- `terminate` - выключение Jarvis

**Рекомендация:** `wake_word_required: false` ✅

---

### Категория 2: Часто используемые команды

**Характеристики:**
- Используются >5 раз в день
- Базовые функции
- Удобство важнее риска

**Команды:**
- `browser_open` - открыть браузер
- `calc_on` / `calc_off` - калькулятор
- `weather` - проверка погоды

**Рекомендация:** `wake_word_required: false` ✅

---

### Категория 3: Voice команды (развлечения)

**Характеристики:**
- Развлекательный контент
- Реакция на разговор
- Высокий риск ложных срабатываний

**Команды:**
- `пошути` / `расскажи анекдот`
- `ты дурак` / `ты глупый`
- `спасибо` / `молодец`
- `пока жди`

**Рекомендация:** `wake_word_required: true` ❌ false

---

### Категория 4: Опасные системные команды

**Характеристики:**
- Могут навредить системе
- Нарушение конфиденциальности
- Необратимые действия

**Команды:**
- Блокировка компьютера (`loginctl lock-session`)
- Скриншоты (`screenshot.exe`)
- Очистка корзины (`Empty trash.exe`)
- Удаление файлов

**Рекомендация:** `wake_word_required: true` ❌ false

---

### Категория 5: Режимы (Modes)

**Характеристики:**
- Переключение состояний системы
- Не предназначены для частого использования
- Могут активироваться случайно

**Команды:**
- `kid_mode_on` / `kid_mode_off`
- `dev_mode_on`
- `check_mode`

**Рекомендация:** `wake_word_required: true` ❌ false

---

### Категория 6: Редко используемые команды

**Характеристики:**
- Используются <1-2 раз в день
- Специфичные действия
- Низкий приоритет удобства

**Команды:**
- `reboot` - перезагрузка Jarvis
- `open_ide` / `close_ide` - IDE (только утром/вечером)
- Steam команды (игровые сессии)

**Рекомендация:** `wake_word_required: true` ❌ false

---

## 📝 Созданная документация

### Файл 1: WAKE_WORD_PROTOCOL.md

**Путь:** `/home/kasiro/Документы/jarvis/resources/commands/WAKE_WORD_PROTOCOL.md`

**Структура:**
1. Что такое `wake_word_required`
2. ✅ МОЖНО помечать false (критические, частые, уникальные)
3. ❌ НЕЛЬЗЯ помечать false (voice, опасные, режимы, редкие)
4. Примеры правильной пометки (5 примеров)
5. Примеры нарушений (4 примера)
6. Чек-лист проверки
7. Технические детали (TOML/YAML синтаксис)
8. Тестирование

**Объём:** ~350 строк

---

### Файл 2: Обновление FIX.md

**Путь:** `/home/kasiro/Документы/jarvis/FIX.md`

**Изменения:**
- Добавлена секция "0. [x] wake_word_required Protocol"
- Статус: ✅ Завершено
- Критерии для `wake_word_required: false`
- Примеры нарушений и правильных примеров

---

## 🔧 Технические детали реализации

### Структура данных

```rust
// crates/jarvis-core/src/commands/structs.rs

#[derive(Serialize, Deserialize, Debug)]
pub struct JCommand {
    // ... другие поля ...
    
    // Wake word requirement: if false, command executes without wake word
    #[serde(default = "default_true")]
    pub wake_word_required: bool,
}

// Helper function for default true value
fn default_true() -> bool {
    true
}
```

### Механизм поиска

```rust
// crates/jarvis-core/src/commands.rs

// Поиск команд БЕЗ wake word
pub fn fetch_command_no_wake_word<'a>(
    phrase: &str,
    commands: &'a [JCommandsList],
) -> Option<(&'a PathBuf, &'a JCommand)> {
    fetch_command_internal(phrase, commands, Some(false))
}

// Внутренняя реализация с фильтром
fn fetch_command_internal<'a>(
    phrase: &str,
    commands: &'a [JCommandsList],
    wake_word_required: Option<bool>,
) -> Option<(&'a PathBuf, &'a JCommand)> {
    for cmd_list in commands {
        for cmd in &cmd_list.commands {
            // Filter by wake_word_required if specified
            if let Some(require_wake) = wake_word_required {
                if cmd.wake_word_required != require_wake {
                    continue;
                }
            }
            // ... поиск по фразам ...
        }
    }
}
```

### Интеграция в STT цикл

```rust
// crates/jarvis-app/src/app.rs

// Проверка команд без wake word
if let Some((cmd_path, cmd_config)) = commands::fetch_command_no_wake_word(&phrase, &commands) {
    // Выполнение команды без wake word
    execute_command(cmd_path, cmd_config);
} else {
    // Обычный цикл с ожиданием wake word
    // ...
}
```

---

## ✅ Результаты

### Созданные файлы

1. **`/home/kasiro/Документы/jarvis/resources/commands/WAKE_WORD_PROTOCOL.md`**
   - Полная документация по `wake_word_required`
   - Примеры правильной пометки
   - Примеры нарушений
   - Чек-лист проверки

2. **`/home/kasiro/Документы/jarvis/FIX.md`** (обновлён)
   - Секция "wake_word_required Protocol"
   - Статус: ✅ Завершено

3. **`/home/kasiro/Документы/jarvis/.qwen/tmp/pickle-rick-sessions/2026-03-09-e5570649/update-docs/research_docs.md`**
   - Этот файл с отчётом

### Охваченные темы

- ✅ Что такое `wake_word_required`
- ✅ Какие команды МОГУТ иметь `wake_word_required: false`
- ✅ Какие команды НЕ МОГУТ иметь `wake_word_required: false`
- ✅ Примеры правильной пометки (5 примеров)
- ✅ Примеры нарушений (4 примера)
- ✅ Чек-лист проверки
- ✅ Технические детали (TOML/YAML, Rust код)
- ✅ Тестирование

---

## 📋 Рекомендации для будущих изменений

### При добавлении новой команды

1. **Определите категорию:**
   - Критическая безопасность?
   - Частое использование?
   - Voice команда?
   - Опасное действие?
   - Режим?
   - Редкое использование?

2. **Примените чек-лист:**
   - ✅ Разрешающие критерии (хотя бы один)
   - ❌ Запрещающие критерии (ни одного)

3. **Установите значение:**
   - Если разрешено → `wake_word_required: false`
   - Иначе → не указывать (по умолчанию `true`)

### При ревью существующих команд

1. Проверить все voice команды → должны иметь `wake_word_required: true`
2. Проверить все опасные команды → должны иметь `wake_word_required: true`
3. Проверить все режимы → должны иметь `wake_word_required: true`
4. Проверить критические команды → должны иметь `wake_word_required: false`
5. Проверить частые команды → могут иметь `wake_word_required: false`

---

## 🔗 Ссылки

- **WAKE_WORD_PROTOCOL.md:** `/home/kasiro/Документы/jarvis/resources/commands/WAKE_WORD_PROTOCOL.md`
- **WAKE_WORD.md:** `/home/kasiro/Документы/jarvis/resources/commands/WAKE_WORD.md`
- **FIX.md:** `/home/kasiro/Документы/jarvis/FIX.md`
- **ADD.md:** `/home/kasiro/Документы/jarvis/ADD.md`
- **commands/structs.rs:** `/home/kasiro/Документы/jarvis/crates/jarvis-core/src/commands/structs.rs`
- **commands.rs:** `/home/kasiro/Документы/jarvis/crates/jarvis-core/src/commands.rs`

---

**Задача выполнена!** 🥒
