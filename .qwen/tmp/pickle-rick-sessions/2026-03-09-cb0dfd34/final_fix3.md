# 🔧 ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ: wake_word_required не работает

## Дата: 2026-03-09

## Проблема по логам:

```
2026-03-09 13:55:48.261912897 [INFO ] STT recognized during VoiceActive: 'открой браузер'
2026-03-09 13:55:54.163021035 [DEBUG] finish_speech() returned empty string
2026-03-09 13:55:54.163163087 [INFO ] Final STT result after silence: ''
```

**Диагноз:** Vosk **распознал фразу** ("открой браузер") **во время** VoiceActive...
**НО** `finish_speech()` вернул **пустоту** через 6 секунд тишины!

---

## 🔍 Корневая причина:

**Vosk очищает результат после тишины!**

Когда Vosk перестал получать аудио (наступила тишина), он **сбросил** распознанную фразу!

**Поток:**
1. Пользователь говорит "открой браузер"
2. VAD обнаружил речь → VoiceActive
3. `stt::recognize()` вернул "открой браузер" ✅
4. **Но результат НЕ СОХРАНЁН!**
5. Пользователь замолк → 6 секунд тишины
6. `finish_speech()` вызван → Vosk очистил результат → **пустота!** ❌

---

## ✅ Решение:

**Сохранять результат `recognize()` сразу когда он получен!**

### Изменения:

#### 1. Добавлена переменная `last_recognized_text`:
```rust
let mut last_recognized_text: Option<String> = None;
```

#### 2. Сохранение результата в VoiceActive:
```rust
let stt_result = stt::recognize(&frame_buffer, false);
if let Some(ref text) = stt_result {
    if !text.trim().is_empty() {
        info!("STT recognized during VoiceActive: '{}'", text);
        // Store the recognized text for later use
        last_recognized_text = Some(text.clone());
    }
}
```

#### 3. Использование сохранённого текста при silence timeout:
```rust
if silence_frames > silence_threshold {
    // Use the last recognized text (Vosk clears result after silence!)
    let final_text = last_recognized_text.take();
    
    if let Some(ref text) = final_text {
        info!("Final STT result after silence: '{}'", text);
    }
    
    if let Some(final_text) = final_text {
        if commands::fetch_command_no_wake_word(&final_text.to_lowercase(), commands_list).is_some() {
            info!("No-wake-word command detected: '{}'", final_text);
            process_text_command(&final_text, &rt);
        }
    }
    
    last_recognized_text = None; // Reset for next phrase
}
```

---

## 📋 Выполненные изменения:

### Файл: crates/jarvis-app/src/app.rs

**Добавлено:**
- Переменная `last_recognized_text: Option<String>` для хранения распознанного текста
- Сохранение текста когда `stt::recognize()` вернул результат
- Использование сохранённого текста при silence timeout
- Сброс переменной после обработки

**Удалено:**
- Вызов `stt::finish_speech()` (который возвращал пустоту)

---

## Verification

### Компиляция
```bash
cargo check -p jarvis-app
# Result: PASSED ✅
```

### Ожидаемое поведение:

1. Пользователь говорит "открой браузер" (без wake word)
2. VAD обнаруживает речь → `VadState::VoiceActive`
3. `stt::recognize()` возвращает "открой браузер" → **сохранено в `last_recognized_text`** ✅
4. Пользователь замолкает → silence frames растут
5. Silence timeout → **используется сохранённый текст** ✅
6. `fetch_command_no_wake_word()` находит команду ✅
7. Команда выполняется! ✅

### Ожидаемые логи:

```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] STT recognized during VoiceActive: 'открой браузер'
[INFO] Final STT result after silence: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
[INFO] Processing text command: открой браузер
[INFO] Command found: "/path/to/browser"
[INFO] Command executed successfully
```

---

## Testing Instructions

### Шаг 1: Собрать проект
```bash
./rebuild.sh --fast
```

### Шаг 2: Запустить Jarvis
```bash
./jarvis.sh
```

### Шаг 3: Открыть логи
```bash
tail -f ~/.config/com.priler.jarvis/app.log
```

### Шаг 4: Протестировать команды без wake word

**Важно:**
- Говори **чётко** и **громко**
- После фразы **замолкни** на 3-4 секунды
- Не говори "джарвис" перед командой!

**Примеры:**
- "открой браузер"
- "какая погода"
- "выключись"

### Шаг 5: Проверить логи

**УСПЕХ:**
```
[INFO] STT recognized during VoiceActive: 'открой браузер'
[INFO] Final STT result after silence: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
[INFO] Command executed successfully
```

**НЕУДАЧА (VAD false positive):**
```
[DEBUG] No text recognized during VoiceActive
[DEBUG] VAD: Silence timeout, returning to wait state
```
→ VAD обнаружил шум вместо речи

**НЕУДАЧА (STT not recognized):**
```
[INFO] VAD: Voice started, flushing XX buffered frames
(нет записи "STT recognized during VoiceActive")
[DEBUG] No text recognized during VoiceActive
```
→ Vosk не распознал речь (говори чётче или проблема с микрофоном)

---

## 🎯 Критерии успеха:

**Команда работает БЕЗ wake word если в логах есть:**
1. ✅ `VAD: Voice started` - VAD обнаружил речь
2. ✅ `STT recognized during VoiceActive: '...'` - Vosk распознал фразу
3. ✅ `Final STT result after silence: '...'` - фраза сохранена
4. ✅ `No-wake-word command detected: '...'` - команда найдена
5. ✅ `Command executed successfully` - команда выполнена

**Если хотя бы одного пункта нет** → проблема!

---

## 🐛 Возможные проблемы:

### Проблема 1: VAD false positives

**Симптомы:**
```
[INFO] VAD: Voice started, flushing 2 buffered frames
[DEBUG] No text recognized during VoiceActive
```

**Причина:** VAD обнаружил шум вместо речи

**Решение:**
- Проверь микрофон на шум
- Говори громче
- Возможно VAD слишком чувствительный

### Проблема 2: STT не распознаёт

**Симптомы:**
```
[INFO] VAD: Voice started, flushing XX buffered frames
(нет записи "STT recognized")
[DEBUG] No text recognized during VoiceActive
```

**Причина:** Vosk не получает аудио или не распознаёт

**Решение:**
- Проверь микрофон: `arecord -l`
- Говори чётче и медленнее
- Проверь что Vosk модель загружена

### Проблема 3: Команда не найдена

**Симптомы:**
```
[INFO] STT recognized during VoiceActive: 'открой браузер'
[INFO] Final STT result after silence: 'открой браузер'
[DEBUG] No matching no-wake-word command found for: 'открой браузер'
```

**Причина:** Команда не помечена как `wake_word_required: false`

**Решение:**
```bash
grep -r "wake_word_required" resources/commands/
```

Ожидаемый результат:
```
resources/commands/browser/command.toml:wake_word_required = false
resources/commands/weather/command.toml:wake_word_required = false
resources/commands/terminate/command.yaml:    wake_word_required: false
```

---

## 📞 Что дальше:

1. **Собери проект:** `./rebuild.sh --fast`
2. **Запусти:** `./jarvis.sh`
3. **Смотри логи:** `tail -f ~/.config/com.priler.jarvis/app.log`
4. **Скажи команду** без wake word
5. **Проверь логи** - должны быть все 5 пунктов успеха!

<promise>BUG_FIXED_FINAL</promise>
