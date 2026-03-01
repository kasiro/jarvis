# 🔧 FIX.md - Список проблем с командами (TODO)

## 🚨 Актуальные проблемы

### 1. [ ] AHK команды не работают на Linux

**Статус:** 🔴 Критично

**Проблема:** AHK (AutoHotkey) работает только на Windows

**Затронутые команды:**
- `jarvis` (reboot.ahk)
- `steam` (Open/Close steam.ahk)
- `volume` (Mute/Set sound.ahk)
- `windows` (все 8 команд)

**Решение:** Создать `.sh` альтернативы для Linux

**Пример структуры:**
```
resources/commands/volume/
├── command.yaml
├── ahk/              # Windows
│   └── Mute volume.ahk
└── sh/               # Linux
    └── mute_volume.sh
```

**Linux аналоги:**
- `Mute volume` → `pactl set-sink-mute @DEFAULT_SINK@ toggle`
- `Set sound` → `pactl set-sink-volume @DEFAULT_SINK@`
- `Screenshot` → `gnome-screenshot` или `flameshot`
- `Task manager` → `gnome-system-monitor`
- `Blocking` → `loginctl lock-session` или `gnome-screensaver-command -l`
- `Sleep` → `systemctl suspend`
- `Clipboard` → `wl-paste` или `xclip`
- `Set language` → `setxkbmap us/ru`

---

### 2. [ ] Команды с хардкодом путей

**Статус:** 🟡 Важно

**Проблема:** Хардкод абсолютных путей

**Пример:**
```toml
# ❌ ПЛОХО
cli_cmd = "/home/user/scripts/myscript.sh"

# ✅ ХОРОШО
cli_cmd = "bash"
cli_args = ["-c", "bash sh/myscript.sh"]
```

**Где проверить:**
- [ ] `resources/commands/*/command.toml`
- [ ] `resources/commands/*/command.yaml`

---

### 3. [ ] Нет обработки ошибок в Lua скриптах

**Статус:** 🟡 Важно

**Проблема:** Команды падают без сообщения

**Пример:**
```lua
-- ❌ ПЛОХО
local response = jarvis.http.get(url)
print(response.body)

-- ✅ ХОРОШО
local response = jarvis.http.get(url)
if response.ok then
    jarvis.system.notify("Погода", response.body)
    jarvis.audio.play_ok()
else
    jarvis.log("error", "Failed: " .. (response.error or "unknown"))
    jarvis.audio.play_error()
end
```

**Где проверить:**
- [ ] `resources/commands/weather/script.lua`
- [ ] `resources/commands/weather/set_city.lua`
- [ ] `resources/commands/counter/script.lua`
- [ ] `resources/commands/test_slots/greet.lua`

---

### 4. [ ] Нет timeout у Lua скриптов

**Статус:** 🟡 Важно

**Проблема:** Бесконечное выполнение

**Где добавить:**
```toml
[[commands]]
id = "weather"
type = "lua"
script = "script.lua"
timeout = 5000  # ← Добавить 5 секунд
```

**Проверить:**
- [ ] `weather` command
- [ ] `counter` command
- [ ] `test_slots` command

---

### 5. [ ] Неправильный sandbox у Lua

**Статус:** 🟡 Важно

**Проблема:** `unsafe` sandbox когда не нужен

**Где проверить:**
```toml
[[commands]]
id = "weather"
type = "lua"
sandbox = "standard"  # ← Безопасный по умолчанию
```

**Sandbox уровни:**
| Sandbox | Доступ | Когда |
|---------|--------|-------|
| `standard` | state, context, log, notify, audio | Обычные команды |
| `unsafe` | + http, file system | Только если нужен HTTP |

---

### 6. [ ] Нет звуковых эффектов

**Статус:** 🟡 Важно

**Проблема:** Команды выполняются без звука

**Где добавить:**
```toml
[[commands]]
id = "my_command"
sounds.ru = ["ok1", "ok2"]  # ← Добавить
sounds.en = ["ok1"]
```

**Проверить:**
- [ ] Все команды в `resources/commands/`

---

### 7. [ ] Команды не кроссплатформенные

**Статус:** 🟡 Важно

**Проблема:** Работают только на одной ОС

**Пример:**
```toml
# ❌ Только Linux
cli_cmd = "gnome-screenshot"

# ✅ Кроссплатформенно
cli_cmd = "bash"
cli_args = ["-c", """
if command -v gnome-screenshot &> /dev/null; then
    gnome-screenshot
elif command -v powershell.exe &> /dev/null; then
    powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('{PRTSC}')"
else
    exit 1
fi
"""]
```

---

## 🧪 ТЕСТОВЫЕ исправления (требуют проверки)

### 9. [ ] `action: voice` не работает

**Статус:** 🟡 **ТЕСТОВОЕ ИСПРАВЛЕНИЕ** (требуется проверка!)

**Проблема:** Команды с `action: voice` не воспроизводят звуки

**Затронутые команды:**
- `jarvis` (stupid, thanks, joke)

**Решение:** Исправить `execute_command` в `crates/jarvis-core/src/commands.rs`

**Файл:** `crates/jarvis-core/src/commands.rs`

**⚠️ ВАЖНО:** Исправление тестовое! Нужно проверить:
- [ ] `cargo check --package jarvis-core`
- [ ] `./rebuild.sh --fast`
- [ ] Тест: сказать "ты дурак" → должен воспроизвестись звук `stupid`
- [ ] Тест: сказать "спасибо" → должен воспроизвестись звук `thanks`
- [ ] Тест: сказать "расскажи анекдот" → должен воспроизвестись звук `joke1-5`

---

## ✅ Исправленные проблемы

### 8. [x] Команды используют `cmd /C` на Linux

---

## 🛠️ Лучшие практики

### 1. TOML формат (рекомендуется)

```toml
# ✅ TOML
[[commands]]
id = "my_command"
type = "cli"

# ❌ YAML (устаревший)
list:
- command:
    action: cli
```

---

### 2. Разделяй Linux и Windows

```
resources/commands/my_command/
├── command.toml
├── sh/           # Linux
│   └── script.sh
└── ahk/          # Windows
    └── script.ahk
```

---

### 3. Обработка ошибок

**Shell:**
```bash
#!/bin/bash
set -e

if ! command -v required_tool &> /dev/null; then
    echo "Error: required_tool not found"
    exit 1
fi

required_tool do_something
```

**Lua:**
```lua
local success, result = pcall(function()
    -- твой код
end)

if success then
    jarvis.audio.play_ok()
else
    jarvis.log("error", "Failed: " .. tostring(result))
    jarvis.audio.play_error()
end
```

---

### 4. State для хранения

```lua
-- Сохранить
jarvis.state.set("last_city", "Moscow")

-- Прочитать
local city = jarvis.state.get("last_city") or "Moscow"

-- Удалить
jarvis.state.delete("last_city")
```

---

### 5. Логирование

```lua
jarvis.log("info", "Command started")
jarvis.log("warn", "Something suspicious")
jarvis.log("error", "Something went wrong")
```

---

## ✅ Чек-лист исправлений

- [ ] Команда работает на Linux
- [ ] Команда работает на Windows (если нужно)
- [ ] Есть обработка ошибок
- [ ] Есть звуковые эффекты
- [ ] Есть timeout для Lua
- [ ] Правильный sandbox
- [ ] Нет хардкода путей
- [ ] Логирует ошибки
- [ ] Проверяет зависимости

---

## 🔗 Ссылки

- `ADD.md` - список команд для реализации
- `QWEN.md` - архитектура проекта
- [TOML формат](https://toml.io/)
- [Lua документация](https://www.lua.org/manual/)
