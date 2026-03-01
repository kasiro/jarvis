# 📝 ADD.md - Список команд для реализации (TODO)

## 🎯 Новые команды

### 1. [ ] `open_terminal` - Открыть терминал

**Описание:** Открывает терминал (gnome-terminal, konsole, или Windows terminal)

**Фразы:**
- RU: "открой терминал", "запусти терминал"
- EN: "open terminal", "launch terminal"

**Тип:** `cli`

**Реализация:**
```toml
[[commands]]
id = "open_terminal"
type = "cli"
cli_cmd = "bash"
cli_args = ["-c", """
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal
elif command -v konsole &> /dev/null; then
    konsole
elif command -v cmd.exe &> /dev/null; then
    start cmd
else
    echo 'Terminal not found'
    exit 1
fi
"""]
sounds.ru = ["ok1", "ok2"]
sounds.en = ["ok1"]

phrases.ru = ["открой терминал", "запусти терминал"]
phrases.en = ["open terminal", "launch terminal"]
```

---

### 2. [ ] `file_manager` - Открыть файловый менеджер

**Описание:** Открывает файловый менеджер (Nautilus, Dolphin, или Explorer)

**Фразы:**
- RU: "открой файлы", "проводник"
- EN: "open file manager", "explorer"

**Тип:** `cli`

---

### 3. [ ] `system_info` - Информация о системе

**Описание:** Показывает информацию о системе (CPU, RAM, диск)

**Фразы:**
- RU: "информация о системе", "покажи систему"
- EN: "system info", "show system"

**Тип:** `lua`

**Реализация:** Использовать `jarvis_core::sysinfo`

---

### 4. [ ] `search_web` - Поиск в интернете

**Описание:** Ищет запрос в Google/Yandex

**Фразы:**
- RU: "найди {query}", "поиск {query}"
- EN: "search {query}", "find {query}"

**Тип:** `cli`

**Слоты:** `query` (text)

---

### 5. [ ] `youtube_play` - Воспроизвести YouTube

**Описание:** Открывает видео на YouTube

**Фразы:**
- RU: "включи на youtube {query}"
- EN: "play on youtube {query}"

**Тип:** `cli`

**Слоты:** `query` (text)

---

## 📚 Существующие команды (требуют проверки)

### [ ] `browser` - Браузер

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/browser/command.toml`

**Проверить:**
- [ ] Работает на Linux
- [ ] Работает на Windows
- [ ] Все фразы RU/EN
- [ ] Звуки есть

---

### [ ] `calculator` - Калькулятор

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/calculator/command.yaml`

**Проверить:**
- [ ] `gnome-calculator` установлен
- [ ] Альтернатива для Windows

---

### [ ] `counter` - Счётчик

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/counter/command.toml`

**Проверить:**
- [ ] Lua скрипт работает
- [ ] Состояние сохраняется

---

### [ ] `jarvis` - Ответы Jarvis

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/jarvis/command.yaml`

**Проверить:**
- [ ] AHK только для Windows
- [ ] Voice команды работают

---

### [ ] `steam` - Steam

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/steam/command.yaml`

**Проверить:**
- [ ] AHK только для Windows
- [ ] Нужен Linux аналог

---

### [ ] `stop` - Остановить

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/stop/command.yaml`

**Проверить:**
- [ ] `stop_chaining` работает

---

### [ ] `terminate` - Выключить

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/terminate/command.yaml`

**Проверить:**
- [ ] `terminate` работает на всех платформах

---

### [ ] `test_slots` - Тест слотов

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/test_slots/command.toml`

**Проверить:**
- [ ] Slot extraction работает

---

### [ ] `volume` - Громкость

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/volume/command.yaml`

**Проверить:**
- [ ] AHK только для Windows
- [ ] Нужен Linux аналог (pactl)

---

### [ ] `weather` - Погода

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/weather/command.toml`

**Проверить:**
- [ ] wttr.in API работает
- [ ] Lua скрипт работает
- [ ] Слот `city` извлекается

---

### [ ] `windows` - Windows команды

**Статус:** ⚠️ Требует проверки

**Файл:** `resources/commands/windows/command.yaml`

**Проверить:**
- [ ] AHK только для Windows
- [ ] Нужны Linux аналоги для:
  - [ ] Свернуть окна
  - [ ] Очистить корзину
  - [ ] Диспетчер задач
  - [ ] Скриншот
  - [ ] Блокировка
  - [ ] Спящий режим
  - [ ] Буфер обмена
  - [ ] Язык

---

## ✅ Чек-лист для новой команды

- [ ] Уникальный `id`
- [ ] Фразы RU
- [ ] Фразы EN
- [ ] Звуки RU
- [ ] Звуки EN
- [ ] Тип команды (cli/lua/voice)
- [ ] Скрипты (sh/ahk/lua)
- [ ] Тест на Linux
- [ ] Тест на Windows (если нужно)
- [ ] Документация

---

## 🔗 Ссылки

- `resources/commands/FIX.md` - проблемы с командами
- `QWEN.md` - архитектура проекта
