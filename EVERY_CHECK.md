# ✅ EVERY_CHECK.md - Чек-лист для каждой сессии

**Проверяй этот файл КАЖДЫЙ раз перед началом работы!**

---

## ⚠️ Важно: Кто что запускает

### 🤖 AI ассистент (Pickle Rick):

**МОЖЕТ:**
- ✅ Читать документацию
- ✅ Проверять git статус
- ✅ Анализировать файлы команд
- ✅ Редактировать код
- ✅ Обновлять документацию
- ✅ `cargo test` - запуск тестов

**НЕ МОЖЕТ (только пользователь):**
- ❌ `./rebuild.sh` - сборка проекта
- ❌ `./jarvis.sh` - запуск приложения
- ❌ `cargo build` - компиляция
- ❌ `cargo check` - проверка компиляции

---

## 🔍 Перед началом работы

### 1. Прочитать документацию

- [ ] **QWEN.md** - последняя информация о проекте
- [ ] **ADD.md** - список функций для реализации
- [ ] **FIX.md** - список проблем для исправления
- [ ] **INSTRUCTION.md** - процесс работы

### 2. Проверить состояние проекта

```bash
# Git статус (может AI)
git status

# Последние коммиты (может AI)
git log -5
```

---

## 🧪 После изменений

### 1. Проверка кода (может AI)

```bash
# Запустить тесты
cargo test --workspace
cargo test -p jarvis-core
```

### 2. Проверка команд (может AI)

```bash
# Перечислить все команды
ls resources/commands/

# Проверить файлы команд
for f in resources/commands/*/command.toml; do
    echo "Checking: $f"
    cat "$f"
done
```

### 3. Проверка сборок (только пользователь!)

⚠️ **Эти команды запускает ТОЛЬКО пользователь!**

```bash
# Быстрая сборка (тест)
./rebuild.sh --fast

# Полная сборка
./rebuild.sh --clean

# Проверка компиляции
cargo check
cargo check --workspace
cargo check -p jarvis-core
```

---

## 🎯 Проверка команд (Commands)

### Таблица проверки

| Команда | Linux | Windows | Фразы RU | Фразы EN | Звуки | Статус |
|---------|-------|---------|----------|----------|-------|--------|
| [`browser`](#browser) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`calculator`](#calculator) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`counter`](#counter) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`jarvis`](#jarvis) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`steam`](#steam) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`stop`](#stop) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`terminate`](#terminate) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`test_slots`](#test_slots) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`volume`](#volume) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`weather`](#weather) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |
| [`windows`](#windows) | ⬜ | ⬜ | ⬜ | ⬜ | ⬜ | ❓ |

---

### Детальная проверка

#### `browser`
- [ ] Linux: `xdg-open` работает
- [ ] Windows: `start` работает
- [ ] Фразы RU: 5 штук
- [ ] Фразы EN: 4 штуки
- [ ] Звуки: ok1-4
- [ ] Файл: `resources/commands/browser/command.toml`

#### `calculator`
- [ ] Linux: `gnome-calculator` установлен
- [ ] Windows: альтернатива есть
- [ ] Фразы RU: 5 штук
- [ ] Фразы EN: 5 штук
- [ ] Звуки: ok1-3
- [ ] Файл: `resources/commands/calculator/command.yaml`

#### `counter`
- [ ] Lua скрипт работает
- [ ] Состояние сохраняется
- [ ] Фразы RU: 1 штука
- [ ] Фразы EN: 2 штуки
- [ ] Звуки: нет (нужно добавить)
- [ ] Файл: `resources/commands/counter/command.toml`

#### `jarvis`
- [ ] AHK только Windows
- [ ] Voice команды работают
- [ ] Фразы RU: много
- [ ] Фразы EN: много
- [ ] Звуки: разные
- [ ] Файл: `resources/commands/jarvis/command.yaml`

#### `steam`
- [ ] AHK только Windows
- [ ] Linux аналог нужен
- [ ] Фразы RU: 6 штук
- [ ] Фразы EN: 6 штук
- [ ] Звуки: ok1-4
- [ ] Файл: `resources/commands/steam/command.yaml`

#### `stop`
- [ ] `stop_chaining` работает
- [ ] Фразы RU: 9 штук
- [ ] Фразы EN: нет (нужно добавить)
- [ ] Звуки: ok1, thanks
- [ ] Файл: `resources/commands/stop/command.yaml`

#### `terminate`
- [ ] `terminate` работает везде
- [ ] Фразы RU: 10 штук
- [ ] Фразы EN: нет (нужно добавить)
- [ ] Звуки: off
- [ ] Файл: `resources/commands/terminate/command.yaml`

#### `test_slots`
- [ ] Slot extraction работает
- [ ] Lua скрипт работает
- [ ] Фразы RU: 2 штуки
- [ ] Фразы EN: 2 штуки
- [ ] Звуки: нет (нужно добавить)
- [ ] Файл: `resources/commands/test_slots/command.toml`

#### `volume`
- [ ] AHK только Windows
- [ ] Linux аналог: `pactl`
- [ ] Фразы RU: много
- [ ] Фразы EN: нет (нужно добавить)
- [ ] Звуки: ok1-4
- [ ] Файл: `resources/commands/volume/command.yaml`

#### `weather`
- [ ] wttr.in API работает
- [ ] Lua скрипт работает
- [ ] Слот `city` извлекается
- [ ] Фразы RU: 2 штуки
- [ ] Фразы EN: 2 штуки
- [ ] Звуки: weather_ru_1-2
- [ ] Файл: `resources/commands/weather/command.toml`

#### `windows`
- [ ] AHK только Windows
- [ ] Linux аналоги нужны:
  - [ ] Свернуть окна: `xdotool key super+d`
  - [ ] Очистить корзину: `rm -rf ~/.local/share/Trash/*`
  - [ ] Диспетчер задач: `gnome-system-monitor`
  - [ ] Скриншот: `gnome-screenshot`
  - [ ] Блокировка: `loginctl lock-session`
  - [ ] Спящий режим: `systemctl suspend`
  - [ ] Буфер обмена: `wl-paste` или `xclip`
  - [ ] Язык: `setxkbmap us/ru`
- [ ] Фразы RU: много
- [ ] Фразы EN: нет (нужно добавить)
- [ ] Звуки: ok1-4
- [ ] Файл: `resources/commands/windows/command.yaml`

---

## 📝 Обновление документации

После любых изменений:

- [ ] **ADD.md** - если реализовал функцию (отметить ✅)
- [ ] **FIX.md** - если исправил проблему (отметить ✅)
- [ ] **EVERY_CHECK.md** - если изменилась проверка
- [ ] **QWEN.md** - если изменилась архитектура
- [ ] **resources/commands/ADD.md** - если добавил команду
- [ ] **resources/commands/FIX.md** - если исправил команду

---

## 🚀 Чек-лист перед коммитом

### Может AI:
- [ ] `cargo test --workspace` - запустить тесты
- [ ] Все команды проверены (таблица выше)
- [ ] Документация обновлена (ADD/FIX отмечены)

### Только пользователь:
- [ ] `cargo check --workspace` - проверить компиляцию
- [ ] `./rebuild.sh --fast` - быстрая сборка
- [ ] Git commit с понятным сообщением

**Опционально:**
- [ ] `cargo clippy --workspace` - линтер
- [ ] `cargo fmt --workspace` - форматирование

---

## 📞 Экстренная проверка

Если что-то сломалось:

1. **Проверить FIX.md** - есть ли известная проблема
2. **Проверить логи:**
   ```bash
   tail -f ~/.config/com.priler.jarvis/app.log
   ```
3. **Пересобрать с очисткой (пользователь!):**
   ```bash
   ./rebuild.sh --clean
   ```
4. **Проверить команды:**
   ```bash
   ls resources/commands/*/command.toml
   ```

---

## 🎯 Приоритеты

| Приоритет | Задача | Кто делает | Статус |
|-----------|--------|------------|--------|
| 🔴 **Критично** | jarvis-app компилируется | 👤 Пользователь | ⬜ |
| 🟡 **Важно** | Команды работают | 🤖 AI + 👤 | ⬜ |
| 🟢 **Нормально** | GUI компилируется | 👤 Пользователь | ⬜ |
| 🔵 **Желательно** | Тесты проходят | 🤖 AI | ⬜ |
| 🟣 **Проверка** | cargo check | 👤 Пользователь | ⬜ |

**Условные обозначения:**
- 🤖 AI - может делать AI ассистент
- 👤 Пользователь - делает только пользователь

---

## 🔗 Быстрые команды

### Может AI:
```bash
# Прочитать документацию
cat QWEN.md
cat ADD.md
cat FIX.md
cat EVERY_CHECK.md

# Проверить git
git status
git log -5

# Проверить команды
ls resources/commands/
cat resources/commands/*/command.toml

# Запустить тесты
cargo test --workspace
cargo test -p jarvis-core
```

### Только пользователь:
```bash
# Собрать
./rebuild.sh --fast    # Быстро
./rebuild.sh --clean   # Полная очистка

# Запустить приложение
./jarvis.sh

# Проверка компиляции
cargo check --workspace
cargo check -p jarvis-core
cargo check -p jarvis-app
cargo check -p jarvis-gui

# Релизная сборка
cargo build --release
```

---

**Запомни: Проверяй этот файл КАЖДЫЙ раз!** 🥒

**И помни: `rebuild.sh` и `jarvis.sh` запускает ТОЛЬКО пользователь!** ⚠️
