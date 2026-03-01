# Rust Code Style Guide

## Naming Conventions

### General Rules
- **Modules & Files**: `snake_case` (e.g., `speech_recognition.rs`)
- **Types (struct, enum, trait)**: `PascalCase` (e.g., `SpeechRecognizer`)
- **Functions & Methods**: `snake_case` (e.g., `process_command()`)
- **Variables**: `snake_case` (e.g., `user_input`)
- **Constants**: `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`)
- **Lifetimes**: Lowercase, short (e.g., `'a`, `'ctx`)

### Examples
```rust
// ✅ Good
mod voice_commands;
struct CommandProcessor;
fn process_audio(&self, samples: &[f32]) -> Result<String>;
let max_volume = 100;
const DEFAULT_TIMEOUT: Duration = Duration::from_secs(5);

// ❌ Bad
mod VoiceCommands;
struct command_processor;
fn ProcessAudio(&self, Samples: &[f32]);
```

## Code Organization

### Module Structure
```rust
// crates/jarvis-core/src/lib.rs
pub mod stt;
pub mod tts;
pub mod commands;
pub mod wake_word;

pub use stt::SpeechRecognizer;
pub use commands::CommandExecutor;
```

### Import Order
1. Standard library (`std::`, `core::`)
2. External crates (`serde::`, `tokio::`)
3. Internal modules (`crate::`)

```rust
use std::path::Path;
use std::sync::Arc;

use serde::{Deserialize, Serialize};
use tokio::sync::Mutex;

use crate::commands::Command;
use crate::config::Config;
```

## Error Handling

### Use Result with Context
```rust
// ✅ Good - with context
fn load_model(path: &Path) -> Result<Model> {
    let data = std::fs::read(path)
        .with_context(|| format!("Failed to read model from {:?}", path))?;
    Ok(Model::from_bytes(&data)?)
}

// ❌ Bad - unwrap in production code
fn load_model(path: &Path) -> Model {
    let data = std::fs::read(path).unwrap(); // PANIC!
    Model::from_bytes(&data).unwrap()
}
```

### Custom Error Types
```rust
#[derive(Debug, thiserror::Error)]
pub enum JarvisError {
    #[error("STT failed: {0}")]
    SttError(#[from] vosk::Error),
    
    #[error("Command not found: {command}")]
    CommandNotFound { command: String },
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, JarvisError>;
```

## Documentation

### Doc Comments
```rust
/// Распознает голосовую команду из аудио потока.
///
/// # Arguments
/// * `samples` - Аудио семплы (48kHz, mono, f32)
/// * `timeout` - Максимальное время ожидания команды
///
/// # Returns
/// * `Ok(String)` - Распознанная команда
/// * `Err(JarvisError)` - Ошибка распознавания
///
/// # Example
/// ```
/// let recognizer = SpeechRecognizer::new()?;
/// let command = recognizer.recognize(&samples, Duration::from_secs(5))?;
/// ```
pub fn recognize(&self, samples: &[f32], timeout: Duration) -> Result<String>;
```

### Module-level Docs
```rust
//! Speech-To-Text модуль для распознавания голоса.
//!
//! Поддерживает следующие движки:
//! - **Vosk** - основной движок (offline)
//! - **Rustpotter** - wake word detection
//!
//! # Example
//! ```rust
//! use jarvis_core::stt::SpeechRecognizer;
//!
//! let stt = SpeechRecognizer::default()?;
//! let text = stt.recognize(audio_samples)?;
//! ```
```

## Async & Concurrency

### Async Functions
```rust
// ✅ Good - async with proper error handling
pub async fn fetch_weather(city: &str) -> Result<Weather> {
    let response = reqwest::get(format!("https://api.weather/{}", city))
        .await?;
    
    if !response.status().is_success() {
        return Err(JarvisError::ApiError(response.status().to_string()));
    }
    
    Ok(response.json().await?)
}
```

### Thread Safety
```rust
// ✅ Good - Arc<Mutex<T>> for shared state
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct JarvisState {
    volume: Arc<Mutex<u8>>,
    is_listening: Arc<AtomicBool>,
}

impl JarvisState {
    pub async fn set_volume(&self, level: u8) {
        let mut volume = self.volume.lock().await;
        *volume = level;
    }
}
```

## Testing

### Unit Tests
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_command_parser() {
        let cmd = parse_command("открыть браузер");
        assert_eq!(cmd.action, "open");
        assert_eq!(cmd.target, "browser");
    }
    
    #[tokio::test]
    async fn test_async_weather_fetch() {
        let weather = fetch_weather("Moscow").await.unwrap();
        assert!(weather.temperature.is_some());
    }
}
```

### Test Organization
```
crates/jarvis-core/
├── src/
│   ├── lib.rs
│   ├── stt.rs
│   └── tests/
│       ├── stt_tests.rs
│       └── command_tests.rs
```

## Performance

### Avoid Unnecessary Allocations
```rust
// ✅ Good - borrow instead of clone
fn process_commands(commands: &[Command]) -> Vec<String> {
    commands.iter().map(|cmd| cmd.name()).collect()
}

// ❌ Bad - unnecessary cloning
fn process_commands(commands: Vec<Command>) -> Vec<String> {
    commands.into_iter().map(|cmd| cmd.name().to_string()).collect()
}
```

### Use Appropriate Data Structures
```rust
// ✅ Good - HashMap for O(1) lookup
use std::collections::HashMap;

let mut commands: HashMap<String, CommandFn> = HashMap::new();
commands.insert("open".to_string(), open_handler);

// ❌ Bad - Vec for lookups
let commands: Vec<(String, CommandFn)> = vec![...];
```

## Cargo.toml Guidelines

### Dependency Organization
```toml
[package]
name = "jarvis-core"
version = "0.1.0"
edition = "2021"
authors = ["Abraham Tugalov"]
license = "GPL-3.0-only"

[dependencies]
# Core
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
log = "0.4"

# Async
tokio = { version = "1", features = ["full"] }

# STT/TTS
vosk = "0.3"
rustpotter = { git = "https://github.com/Priler/rustpotter" }

# Optional (platform-specific)
[target.'cfg(target_os = "linux")'.dependencies]
notify-rust = "4"

[target.'cfg(target_os = "windows")'.dependencies]
winrt-notification = "0.5"

[dev-dependencies]
tokio-test = "0.4"
tempfile = "3"
```

## Code Review Checklist

- [ ] Нет `unwrap()` в production коде
- [ ] Все публичные функции имеют документацию
- [ ] Ошибки обрабатываются через `Result`
- [ ] Нет лишних аллокаций (`.clone()`, `.to_string()`)
- [ ] Async функции используют `.await` корректно
- [ ] Тесты покрывают критическую логику
- [ ] `cargo clippy` без предупреждений
- [ ] `cargo fmt` применен

---

**Based on**: Rust API Guidelines, Google Rust Style Guide  
**Last Updated**: 2026-02-23
