# Fix: wake_word_required не работает - команда требует wake word

## Дата: 2026-03-09
## Проблема: Команды без wake word всё равно требуют wake word

## Анализ проблемы

### Предыдущая ошибка:
`finish_speech()` был добавлен в `recognize_command()` который **НИКОГДА не вызывается** без wake word!

**Архитектурная проблема:**
```
'wake_word: loop {
    match vad_state {
        VadState::WaitingForVoice => { ... }
        VadState::VoiceActive => {
            if wake_word_detected {
                recognize_command()  // ← Вызывается ТОЛЬКО после wake word!
            }
            if silence_timeout {
                // finish_speech() здесь - но это внутри recognize_command()!
            }
        }
    }
}
```

### Корневая причина:
- `recognize_command()` вызывается **ТОЛЬКО** после детекции wake word
- Команды без wake word **никогда не достигают** `recognize_command()`
- Проверка `fetch_command_no_wake_word()` должна быть **ВНЕ** `recognize_command()`

## Решение

Переместить проверку команд без wake word **в основной цикл** `VadState::VoiceActive`:

```rust
VadState::VoiceActive => {
    if silence_frames > silence_threshold {
        // Check for no-wake-word commands BEFORE returning to wait state
        if let Some(final_text) = stt::finish_speech() {
            if !final_text.trim().is_empty() {
                if commands::fetch_command_no_wake_word(&final_text, commands_list).is_some() {
                    // No-wake-word command found - execute it!
                    process_text_command(&final_text, &rt);
                }
            }
        }
    }
}
```

## Выполненные изменения

### Файл: crates/jarvis-app/src/app.rs

**Изменён основной цикл `'wake_word: loop`:**
- Добавлена проверка `finish_speech()` при silence timeout
- Проверка `fetch_command_no_wake_word()` в основном цикле
- Выполнение `process_text_command()` для команд без wake word

**Ключевое изменение:**
```rust
if silence_frames > silence_threshold {
    // Check for no-wake-word commands BEFORE returning to wait state
    if let Some(final_text) = stt::finish_speech() {
        if !final_text.trim().is_empty() {
            if commands::fetch_command_no_wake_word(&final_text.to_lowercase(), commands_list).is_some() {
                // No-wake-word command found - execute it!
                info!("No-wake-word command detected: '{}'", final_text);
                process_text_command(&final_text, &rt);
            }
        }
    }
    
    vad_state = VadState::WaitingForVoice;
    // ... reset recognizers
}
```

## Verification

### Компиляция
```bash
cargo check -p jarvis-app
# Result: PASSED ✅
```

### Ожидаемое поведение:

1. Пользователь говорит "открой браузер" **БЕЗ** wake word
2. VAD обнаруживает речь → `VadState::VoiceActive`
3. Пользователь замолкает → silence frames растут
4. Silence timeout → вызов `finish_speech()`
5. Vosk возвращает "открой браузер"
6. `fetch_command_no_wake_word()` находит команду ✅
7. `process_text_command()` выполняет команду ✅
8. Jarvis открывает браузер!

### Логи которые должны появиться:
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] Final STT result after silence: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
[INFO] Processing text command: открой браузер
[INFO] Command executed successfully
```

## Testing Instructions

1. Собрать проект:
   ```bash
   ./rebuild.sh --fast
   ```

2. Запустить Jarvis:
   ```bash
   ./jarvis.sh
   ```

3. **НЕ говоря wake word**, сказать:
   - "открой браузер"
   - "какая погода"
   - "выключись"

4. Проверить логи:
   ```bash
   tail -f ~/.config/com.priler.jarvis/app.log
   ```

## Архитектурные изменения

### БЫЛО (неправильно):
```
'wake_word loop
  └─> VadState::VoiceActive
       └─> if wake_word_detected
            └─> recognize_command()  ← Только с wake word!
                 └─> finish_speech() ← Никогда не вызывается!
```

### СТАЛО (правильно):
```
'wake_word loop
  └─> VadState::VoiceActive
       ├─> if wake_word_detected
       │    └─> recognize_command()  ← Для команд С wake word
       │
       └─> if silence_timeout
            └─> finish_speech()      ← Для команд БЕЗ wake word!
                 └─> fetch_command_no_wake_word()
                      └─> process_text_command()
```

<promise>BUG_FIXED</promise>
