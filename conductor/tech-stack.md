# Technology Stack

## Core Technologies

### Backend
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Language** | Rust | 2021 Edition | Основной язык backend |
| **GUI Framework** | Tauri | Latest | Desktop application framework |
| **Async Runtime** | Tokio | Latest | Асинхронная обработка |
| **State Management** | parking_lot | 0.12.5 | Синхронизация потоков |

### Frontend
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Framework** | Svelte | Latest | UI компоненты |
| **Build Tool** | Vite | Latest | Быстрая сборка |
| **Language** | TypeScript | Strict Mode | Типизация |
| **Styling** | Bootstrap CSS | Latest | UI стили |
| **Design System** | Material Design | Principles | UX/UI принципы |

## AI/ML Stack

### Speech-To-Text (STT)
| Component | Technology | Status | Notes |
| :---- | :---- | :---- | :---- |
| **Primary** | Vosk | ✅ Working | Offline STT, русская модель |
| **Library** | vosk-rs | ✅ Working | Rust bindings для Vosk |

### Wake Word Detection
| Component | Technology | Status | Notes |
| :---- | :---- | :---- | :---- |
| **Primary** | Rustpotter | 🔄 WIP | Rust реализация Porcupine |
| **Fallback** | Vosk | ✅ Working | Медленнее, но работает |
| **Legacy** | Picovoice Porcupine | ⚠️ API Key | Требует ключ |

### Text-To-Speech (TTS)
| Component | Technology | Status | Notes |
| :---- | :---- | :---- | :---- |
| **Current** | В разработке | ⏳ Planned | Выбор движка TBD |
| **Evaluated** | Silero TTS | ❌ Not Used | Нейросетевой TTS |
| **Evaluated** | Coqui TTS | ❌ Not Used | Нейросетевой TTS |
| **Evaluated** | gTTS | ❌ Not Used | Требует интернет |

### Natural Language Understanding (NLU)
| Component | Technology | Status | Notes |
| :---- | :---- | :---- | :---- |
| **Current** | None | ⏳ Planned | Будущая реализация |
| **AI Fallback** | Qwen API | ✅ Working | Локальный прокси |

### Embeddings & Vector Search
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Embeddings** | fastembed | 5.8.1 | Векторные представления |
| **Runtime** | ort | 2.0.0-rc.11 | ONNX Runtime |
| **Tokenization** | tokenizers | 0.22 | Токенизация текста |

## Command System

### Scripting
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Embedding** | mlua | 0.11.5 | Lua скрипты для команд |
| **Lua Version** | Lua 5.4 | Vendored | Встроенная Lua |
| **Config Format** | TOML | 0.9.8 | Конфигурация команд |

### Command Execution
| Platform | Technology | Notes |
| :---- | :---- | :---- |
| **Linux** | bash + xdotool + wmctrl | Нативная поддержка |
| **Windows** | PowerShell + AutoHotkey | Legacy поддержка |

## System Integration

### Notifications
| Platform | Technology | Status |
| :---- | :---- | :---- |
| **Linux** | notify-rust | ✅ Working |
| **Windows** | winrt-notification | ⚠️ Windows only |

### Clipboard
| Platform | Technology | Status |
| :---- | :---- | :---- |
| **Cross-platform** | arboard | ✅ Working |

### Audio
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Playback** | rodio | 0.21 | Воспроизведение звука |
| **Advanced** | kira | 0.11 | Продвинутый аудио движок |
| **Recording** | pv_recorder | Git | Запись с микрофона |
| **Noise Cancellation** | nnnoiseless | 0.5 | Шумоподавление |

### Image Processing
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Library** | image | 0.25 | Обработка изображений |

## System Information

### System Monitoring
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **System Info** | sysinfo | 0.37.2 | Информация о системе |
| **Locale** | sys-locale | 0.3 | Определение локали |

### File & Directory Management
| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Directories** | platform-dirs | 0.3 | Кроссплатформенные пути |
| **Temp Files** | tempfile | 3.24 | Временные файлы |

## Networking

### HTTP Client
| Component | Technology | Version | Features |
| :---- | :---- | :---- | :---- |
| **HTTP** | reqwest | 0.13.1 | blocking, json |
| **WebSocket** | tokio-tungstenite | 0.28.0 | WebSocket клиент |
| **Async** | futures-util | 0.3 | Асинхронные утилиты |

## Data Serialization

| Format | Library | Version |
| :---- | :---- | :---- |
| **JSON** | serde_json | 1.0 |
| **YAML** | serde_yaml | 0.9 |
| **TOML** | toml | 0.9.8 |

## Internationalization

| Component | Technology | Version |
| :---- | :---- | :---- |
| **i18n** | fluent | 0.17.0 |
| **Bundle** | fluent-bundle | 0.16.0 |
| **LangID** | unic-langid | 0.9 |

## Utilities

| Component | Technology | Version | Purpose |
| :---- | :---- | :---- | :---- |
| **Singleton** | once_cell | 1.19 | Lazy инициализация |
| **Logging** | log | 0.4 | Логирование |
| **Random** | rand | 0.8 | Генерация случайных чисел |
| **Diff** | seqdiff | 0.3 | Разница последовательностей |
| **Audio WAV** | hound | 3.5 | WAV файлы |
| **Hashing** | sha2 | 0.10 | SHA-2 хеширование |
| **Regex** | regex | 1 | Регулярные выражения |
| **Date/Time** | chrono | 0.4 | Работа со временем |

## Linux-Specific Dependencies

| Package | Purpose |
| :---- | :---- |
| **webkit2gtk** | Tauri WebView |
| **gtk3** | GTK интерфейс |
| **libappindicator3** | Tray icon для GNOME |
| **libayatana-appindicator** | Альтернативный tray |
| **xdotool** | Управление окнами |
| **wmctrl** | Переключение окон |
| **xclip / wl-clipboard** | Буфер обмена |
| **libnotify** | Системные уведомления |

## Windows-Specific Dependencies

| Package | Purpose | Status |
| :---- | :---- | :---- |
| **winrt-notification** | Уведомления Windows | Windows only |
| **winapi** | Windows API | Windows only |

## Build Tools

| Tool | Purpose |
| :---- | :---- |
| **Cargo** | Rust package manager |
| **npm / yarn** | JavaScript package manager |
| **Tauri CLI** | Tauri build/dev |

## Development Requirements

### Rust
- **Edition**: 2021
- **Toolchain**: Stable (рекомендуется)

### Node.js
- **Version**: 18+ (рекомендуется)
- **Package Manager**: npm или yarn

### System Packages (Arch/CachyOS)
```bash
sudo pacman -S webkit2gtk gtk3 libappindicator libayatana-appindicator
```

### System Packages (Debian/Ubuntu)
```bash
sudo apt install libwebkit2gtk-4.0-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev libgdk-pixbuf2.0-dev
```

### System Packages (Fedora)
```bash
sudo dnf install webkit2gtk3-devel gtk3-devel libappindicator-devel
```

---

## Architecture Notes

### Project Structure
```
jarvis/
├── crates/
│   ├── jarvis-core/    # Ядро: STT, TTS, команды, AI, Lua API
│   ├── jarvis-app/     # Console приложение (backend)
│   ├── jarvis-gui/     # Tauri GUI (frontend + tray)
│   └── jarvis-cli/     # CLI (TODO)
├── resources/
│   ├── commands/       # Lua + bash скрипты команд
│   ├── sound/          # Звуковые файлы
│   ├── models/         # ML модели (Vosk)
│   └── icons/          # Иконки приложения
├── frontend/           # React/Vite/Svelte UI
├── lib/                # Системные библиотеки
└── conductor/          # Conductor документы
```

### Key Design Decisions

1. **Offline-First**: Все критические функции работают без интернета
2. **Privacy-First**: Никакой телеметрии, никаких облаков
3. **Cross-Platform**: Windows + Linux (CachyOS GNOME Wayland)
4. **Rust Core**: Вся бизнес-логика на Rust
5. **Lua Commands**: Гибкая система команд через скрипты
6. **Tauri GUI**: Легковесный GUI вместо Electron

---

**Last Updated**: 2026-02-23  
**Maintained By**: Pickle Rick
