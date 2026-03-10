# Документация: Команды без Wake Word

## 📋 Обзор

Jarvis поддерживает команды которые выполняются **без необходимости** произнесения wake word фразы (например, "Jarvis", "Алиса").

## 🔧 Как добавить команду без wake word

### Для TOML файлов

Добавьте поле `wake_word_required = false` в команду:

```toml
[[commands]]
id = "my_command"
type = "python"
script = "my_script.py"
wake_word_required = false  # ← Команда работает без wake word

phrases.ru = [
    "моя команда",
    "выполни действие",
]
```

### Для YAML файлов

Добавьте поле `wake_word_required: false` в команду:

```yaml
list:
- command:
    action: python
    script: my_script.py
    wake_word_required: false  # ← Команда работает без wake word
  phrases:
  - моя команда
  - выполни действие
```

## ⚠️ Важные замечания

### Обратная совместимость
- По умолчанию `wake_word_required = true`
- Старые команды без поля требуют wake word
- Это обеспечивает обратную совместимость

### Какие команды помечать

**Рекомендуется `wake_word_required: false` для:**

1. **Критические команды:**
   - `terminate` - выключение Jarvis
   - `stop_chaining` - остановка выполнения

2. **Часто используемые команды:**
   - `browser_open` - открыть браузер
   - `calculator` - калькулятор
   - `weather` - погода

**НЕ рекомендуется `wake_word_required: false` для:**

1. **Опасные команды:**
   - Удаление файлов
   - Изменение системных настроек
   - Платежи и транзакции

2. **Редко используемые команды:**
   - Специфичные действия
   - Сложные сценарии

## 🎯 Архитектура

### Как это работает

1. **STT распознаёт фразу**
2. **Проверка команд без wake word:**
   - `commands::fetch_command_no_wake_word()` ищет команды с `wake_word_required: false`
   - Если найдена - выполняет немедленно
3. **Если не найдена:**
   - Обычный цикл с wake word
   - `commands::fetch_command()` ищет все команды

### Файлы

- `crates/jarvis-core/src/commands/structs.rs` - структура команды
- `crates/jarvis-core/src/commands.rs` - функции поиска команд
- `crates/jarvis-app/src/app.rs` - интеграция в STT цикл

## 📝 Примеры

### Пример 1: Команда выключения

```yaml
# resources/commands/terminate/command.yaml
list:
- command:
    action: terminate
    wake_word_required: false  # Можно сказать "выключись" без "Jarvis"
  phrases:
  - выключись
  - вырубись
  - закройся
```

### Пример 2: Команда открытия браузера

```toml
# resources/commands/browser/command.toml
[[commands]]
id = "browser_open"
type = "python"
script = "sh/open_browser.py"
wake_word_required = false  # Можно сказать "открой браузер" без "Jarvis"

phrases.ru = [
    "открой браузер",
    "запусти браузер",
]
```

## 🧪 Тестирование

После добавления команды:

1. **Проверка компиляции:**
   ```bash
   cargo check -p jarvis-core
   ```

2. **Проверка парсинга:**
   ```bash
   ./rebuild.sh --fast
   ```

3. **Тестирование:**
   - Скажите фразу команды **без** wake word
   - Jarvis должен выполнить команду

## 🔒 Безопасность

**Внимание!** Команды без wake word могут быть активированы случайно. Используйте с осторожностью:

- Проверяйте уникальность фраз
- Не используйте для опасных действий
- Тестируйте на ложные срабатывания
