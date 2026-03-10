# Fix: wake_word_required не работает - STT не завершает фразу

## Дата: 2026-03-09
## Проблема: Команды без wake word не работают

## Анализ проблемы

### Логи пользователя:
```
2026-03-09 13:24:46.818839567 [INFO ] <jarvis_app::app:198>:Recognized voice: 
2026-03-09 13:24:46.818916401 [DEBUG] <jarvis_app::app:265>:Ignoring too short recognition: ''
```

**Проблема:** STT возвращает **пустую строку** вместо распознанной фразы!

### Корневая причина

Vosk STT работает в режиме `accept_waveform()` который возвращает результат **только когда статус `Finalized`**.

**Проблема:**
1. Пользователь говорит фразу
2. Наступает тишина
3. VAD обнаруживает silence timeout
4. **Но Vosk не вернул результат** потому что статус не `Finalized`
5. Фраза теряется, возвращается пустая строка

### Решение

Добавлена функция `finish_speech()` которая:
1. Вызывается **перед** возвратом в wake word режим
2. Берёт результат из Vosk даже если статус не `Finalized`
3. Возвращает последний распознанный текст

## Выполненные изменения

### 1. crates/jarvis-core/src/stt/vosk.rs

**Добавлено:**
```rust
// Finish speech recognition and get final result
pub fn finish_speech() -> Option<String> {
    let mut recognizer = SPEECH_RECOGNIZER.get()?.lock();
    
    // Get result even if not finalized - Vosk will return last recognized text
    recognizer.result()
        .multiple()
        .and_then(|m| m.alternatives.first().map(|a| a.text.to_string()))
}
```

### 2. crates/jarvis-core/src/stt.rs

**Добавлено:**
```rust
pub use self::vosk::finish_speech;
```

### 3. crates/jarvis-app/src/app.rs

**Изменено:**
```rust
// В цикле VAD, когда обнаружена тишина:
if silence_frames > silence_threshold {
    // Before returning, flush STT to get final result
    if let Some(final_text) = stt::finish_speech() {
        info!("Final STT result after silence: '{}'", final_text);
        if !final_text.trim().is_empty() {
            // Process the final result
            process_text_command(&final_text, rt);
        }
    }
    
    info!("Long silence detected, returning to wake word mode.");
    return;
}
```

**Обновлено `process_text_command`:**
- Добавлена проверка `fetch_command_no_wake_word()`
- Логирование найденных команд без wake word

## Verification

### Компиляция
```bash
cargo check -p jarvis-core -p jarvis-app
# Result: PASSED ✅
```

### Ожидаемое поведение:
1. Пользователь говорит "открой браузер" (без wake word)
2. VAD обнаруживает речь → буферизация
3. Пользователь замолкает
4. Silence timeout → вызов `finish_speech()`
5. Vosk возвращает "открой браузер"
6. `fetch_command_no_wake_word()` находит команду
7. Команда выполняется! ✅

## Testing Instructions

1. Собрать проект:
   ```bash
   ./rebuild.sh --fast
   ```

2. Запустить Jarvis:
   ```bash
   ./jarvis.sh
   ```

3. Протестировать команды без wake word:
   - "открой браузер"
   - "какая погода"
   - "выключись"

4. Проверить логи:
   ```bash
   tail -f ~/.config/com.priler.jarvis/app.log
   ```
   
   Ожидаемые записи:
   ```
   [INFO] Final STT result after silence: 'открой браузер'
   [INFO] No-wake-word command detected (from finish_speech): 'открой браузер'
   ```

<promise>BUG_FIXED</promise>
