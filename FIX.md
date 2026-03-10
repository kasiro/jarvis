# 🔧 FIX.md - Список проблем для исправления (TODO)

## 🚨 Актуальные проблемы

### 0. [x] wake_word_required Protocol

**Статус:** ✅ Завершено

**Проблема:** Отсутствовала документация по правильному использованию `wake_word_required`.

**Решение:**
✅ Создан файл `resources/commands/WAKE_WORD_PROTOCOL.md`
✅ Добавлены правила пометки команд
✅ Добавлены примеры нарушений

**Файлы:**
- `resources/commands/WAKE_WORD_PROTOCOL.md` - полная документация

**Критерии для `wake_word_required: false`:**

✅ **МОЖНО помечать false:**
- Критические команды безопасности (`terminate`)
- Часто используемые команды (`browser_open`, `calc_on`, `weather`)
- Команды с уникальными фразами

❌ **НЕЛЬЗЯ помечать false:**
- Voice команды (`пошути`, `расскажи анекдот`, `ты дурак`)
- Опасные команды (блокировка, скриншоты, удаление)
- Режимы (`kid_mode`, `dev_mode`)
- Редко используемые команды

**Примеры нарушений:**
```yaml
# ❌ НАРУШЕНИЕ - voice команда без wake word
- command:
    action: voice
    wake_word_required: false  # ❌ ОШИБКА!
  phrases:
  - расскажи анекдот

# ❌ НАРУШЕНИЕ - опасная команда без wake word
- command:
    action: cli
    cli_cmd: "loginctl lock-session"
    wake_word_required: false  # ❌ ОШИБКА!
  phrases:
  - заблокируй компьютер
```

**Правильные примеры:**
```yaml
# ✅ ПРАВИЛЬНО - критическая команда
- command:
    action: terminate
    wake_word_required: false  # ✅ Должно работать всегда
  phrases:
  - выключись

# ✅ ПРАВИЛЬНО - часто используемая команда
- command:
    action: python
    script: calc_on.py
    wake_word_required: false  # ✅ Удобно для частого использования
  phrases:
  - включи калькулятор
```

---

### 1. [ ] GUI паникует: "webview with label `main` already exists"

**Статус:** 🔴 Критично

**Проблема:**
```
thread 'main' panicked at tauri-2.9.5/src/app.rs:1301:11:
Failed to setup app: error encountered during setup hook: 
a webview with label `main` already exists
```

**Причина:** Окно создаётся дважды:
1. В `tauri.conf.json` → `"windows": [...]`
2. В `main.rs` → `.setup(|app| { WebviewWindow::builder(...) })`

**Решение:**
- Удалить секцию `"windows"` из `tauri.conf.json`
- Окно должно создаваться только в `main.rs`

**Файлы:**
- `crates/jarvis-gui/tauri.conf.json`
- `crates/jarvis-gui/src/main.rs`

---

### 2. [x] Voice команды запускаются несколько раз

**Статус:** ✅ Исправлено

**Проблема:** Voice команды (`пошути`, `расскажи анекдот`) воспроизводят звук **ДВАЖДЫ**.

**Лог:**
```
[INFO] Playing voice sound: joke1.mp3  ← Первый раз (из execute_command)
[INFO] Command executed successfully
[INFO] Playing random sound: joke1.mp3  ← Второй раз (из app.rs)!
```

**Причина:**
- `execute_command` в `jarvis-core` воспроизводил звук для voice команд
- `app.rs` строка 381 **ТОЖЕ** воспроизводила звук после выполнения
- Звук играл **дважды**!

**Решение:**
✅ Не воспроизводить звук в `app.rs` для voice команд

**Файл:** `crates/jarvis-app/src/app.rs`

```rust
// Don't play sound for voice commands - sound already played in execute_command!
if cmd_config.cmd_type != "voice" {
    voices::play_random_from(cmd_config.get_sounds(&i18n::get_language()).as_slice());
}
```

---

### 3. [x] Погода показывает неверный город

**Статус:** ✅ Исправлено

**Проблема:** Команда погоды использовала город по умолчанию **Moscow** вместо **Novosibirsk**.

**Решение:**
✅ Установлен **Novosibirsk** по умолчанию

**Файл:** `resources/commands/weather/script.lua`

```lua
-- Default city: Novosibirsk
local city = jarvis.state.get("city") or "Novosibirsk"
```

**Файл:** `resources/commands/weather/set_city.lua`

```lua
-- Default city: Novosibirsk
local city = "Novosibirsk"

-- try to extract city name from phrase if provided
local extracted_city = phrase:match("город%s+(.+)") or phrase:match("city%s+(.+)")

if extracted_city then
    city = extracted_city
end

jarvis.state.set("city", city)
```

**Команды:**
- "какая погода" → покажет погоду в **Novosibirsk**
- "установи город Москва" → установит **Moscow**
- "поменяй город" → установит **Novosibirsk** (по умолчанию)

---

### 4. [x] YAML команды не работают (калькулятор)

**Статус:** ✅ Исправлено

**Проблема:** YAML команды (`calculator`, `jarvis`, `steam`) **не выполнялись** - `cli_cmd` и `cli_args` были пустыми.

**Лог:**
```
[DEBUG] Spawning: sh -c  []  ← ПУСТЫЕ АРГУМЕНТЫ!
```

**Причина:**
- YAML парсер в `commands.rs` не передавал `cli_cmd` и `cli_args`
- Поля устанавливались в `String::new()` и `Vec::new()`

**Решение:**
✅ Добавлены поля в `LegacyCommandData`
✅ YAML парсер теперь передаёт `cli_cmd` и `cli_args`

**Файл:** `crates/jarvis-core/src/commands/structs.rs`

```rust
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct LegacyCommandData {
    pub action: String,
    #[serde(default)]
    pub exe_path: String,
    #[serde(default)]
    pub exe_args: Vec<String>,
    #[serde(default)]
    pub cli_cmd: String,      // ← Добавлено
    #[serde(default)]
    pub cli_args: Vec<String>, // ← Добавлено
}
```

**Файл:** `crates/jarvis-core/src/commands.rs`

```rust
let cmd = JCommand {
    cli_cmd: legacy.command.cli_cmd.clone(),   // ← Берём из YAML
    cli_args: legacy.command.cli_args.clone(), // ← Берём из YAML
    // ...
};
```

**Команды которые заработали:**
- "включи калькулятор" → `gnome-calculator` ✅
- "закрой калькулятор" → `pkill -i 'gnome-calculator'` ✅

---

### 5. [x] Погода не работает без интернета

**Статус:** ✅ Исправлено

**Проблема:** Команда погоды использовала только **wttr.in API** и не работала при отсутствии интернета.

**Решение:**
✅ Добавлен **fallback через ansiweather**

**Файл:** `resources/commands/weather/script.lua`

```lua
-- Method 1: Try wttr.in API
local response = jarvis.http.get(url)
if response.ok then
    -- show notification
    jarvis.system.notify(title, response.body)
end

-- Method 2: Fallback to ansiweather
local grep_cmd = string.format('ansiweather -l "%s,RU" -u metric -f 1 -a false 2>&1 | grep -oP ".*°C"', city)
local handle = io.popen(grep_cmd)
local weather_output = handle:read("*a")
handle:close()

if weather_output then
    jarvis.system.notify(title, weather_output)
end
```

**Команды:**
- "какая погода" → wttr.in API → ansiweather fallback ✅

---

## ✅ Исправленные проблемы

### 0. [x] 🎵 Jarvis не отвечает звуком СРАЗУ после команды

**Статус:** ✅ Исправлено

**Проблема:** Jarvis воспроизводил звук только **после** завершения всех действий команды (VPN, окна, браузер...), а не **сразу** после получения команды.

**Причина:**
1. Rust код в `execute_python()` использовал `child.wait_with_output()` - **блокирующий** вызов
2. Rust ждал пока Python скрипт **полностью завершится**
3. Python выполнял все действия, и **только потом** воспроизводил звук
4. Rust получал ответ и продолжал работу

**Решение:**
✅ Изменён `execute_python()` в `commands.rs` - **не ждёт** завершения Python
✅ Python процесс **детачится** и работает **в фоне** независимо
✅ Звук воспроизводится **сразу** после получения команды
✅ Rust продолжает работу немедленно

**Файлы:**
- `crates/jarvis-core/src/commands.rs` - асинхронный запуск Python
- `resources/commands/jarvis_api/audio.py` - асинхронное воспроизведение
- `resources/commands/modes/kid_mode_on.py` - звук в начале
- `resources/commands/modes/kid_mode_off.py` - звук в начале
- `resources/commands/modes/dev_mode_on.py` - звук в начале

**Изменения в Rust:**
```rust
// БЫЛО (блокирующее ожидание):
let output = child.wait_with_output()?;

// СТАЛО (асинхронный запуск):
// Отправляем контекст и закрываем stdin
if let Some(_stdin) = child.stdin.take() {
    drop(_stdin);
}

// Детачим процесс - Python работает в фоне
use std::mem;
mem::forget(child);

// Сразу возвращаем успех!
Ok(true)
```

**Изменения в Audio API:**
```python
# Теперь все методы используют асинхронное воспроизведение по умолчанию:
jarvis.audio.play_ok()                    # Асинхронно (blocking=False)
jarvis.audio.play("sound")                # Асинхронно
jarvis.audio.play_error()                 # Асинхронно

# При необходимости можно ждать завершения:
jarvis.audio.play_ok(blocking=True)       # Синхронно
```

**Результат:**
- ✅ Jarvis **сразу** отвечает звуком после команды
- ✅ Действия выполняются **параллельно** с воспроизведением
- ✅ UX улучшен - пользователь слышит ответ **немедленно**

---

### 1. [x] ❌ Сборка зависает на RPM

**Статус:** ✅ Исправлено

**Проблема:** `cargo tauri build` зависает на RPM

**Решение:** Отключить RPM в `tauri.conf.json`
```json
{
  "bundle": {
    "targets": ["app"]
  }
}
```

---

### 3. [x] Команды не выполняются на Linux

**Статус:** ✅ Исправлено

**Проблема:** Команды используют Windows `cmd /C`

**Решение:** Использовать кроссплатформенные скрипты
```toml
cli_cmd = "bash"
cli_args = ["-c", "xdg-open https://example.com"]
```

📚 **Подробно:** `resources/commands/FIX.md`

---

### 4. [x] Lua 5.5 не найден

**Статус:** ✅ Исправлено

**Проблема:** `unable to find library -llua5.5`

**Решение:** Изменить в `Cargo.toml`
```toml
mlua = { version = "0.11.5", features = ["lua54", ...] }
```

---

### 5. [x] Vosk не работает

**Статус:** ✅ Исправлено

**Проблема:** STT не распознаёт речь

**Решение:**
1. Скачать модель: `vosk-model-small-ru-0.22`
2. Распаковать в `resources/vosk/`
3. Пересобрать: `./rebuild.sh --clean`

---

### 6. [x] Микрофон не работает

**Статус:** ✅ Исправлено

**Проблема:** Jarvis не слышит

**Решение:**
```bash
pactl set-default-source <device_name>
```

---

### 7. [x] Трей иконка не видна

**Статус:** ✅ Исправлено

**Проблема:** Wayland не поддерживает GTK tray

**Решение:**
```bash
sudo pacman -S libappindicator-gtk3
export GDK_BACKEND=x11
```

---

### 8. [x] Frontend не собирается

**Статус:** ✅ Исправлено

**Проблема:** `npm run build` падает

**Решение:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 🛠️ Отладка

### Включить логирование
```bash
RUST_LOG=debug cargo run -p jarvis-app
RUST_LOG=debug cargo tauri dev
RUST_BACKTRACE=1 ./jarvis.sh
```

### Просмотр логов
```bash
cat ~/.config/com.priler.jarvis/app.log
tail -f ~/.config/com.priler.jarvis/app.log
```

---

## ✅ Чек-лист исправлений

- [ ] Проблема воспроизводится
- [ ] Лог ошибки сохранён
- [ ] Зависимости проверены
- [ ] Конфиг сброшен
- [ ] Последняя версия Rust
- [ ] `cargo clean` выполнен
- [ ] Пересборка с `--clean`

---

## 🔗 Полезные ссылки

- [Tauri troubleshooting](https://tauri.app/start/troubleshooting/)
- [Rust debugging](https://doc.rust-lang.org/book/ch10-01-syntax.html)
- [Vosk models](https://alphacephei.com/vosk/models)
