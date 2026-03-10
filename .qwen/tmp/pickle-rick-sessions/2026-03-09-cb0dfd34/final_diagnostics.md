# 🔍 Финальная диагностика wake_word_required

## Проблема по логам:

```
2026-03-09 13:45:27.101944290 [INFO ] <jarvis_app::app:74>:VAD: Voice started, flushing 2 buffered frames
2026-03-09 13:45:36.166678232 [DEBUG] <jarvis_core::stt::vosk:114>:finish_speech() returned empty string
2026-03-09 13:45:36.166735504 [INFO ] <jarvis_app::app:130>:Final STT result after silence: ''
```

## Диагноз:

**VAD ложно срабатывает** → обнаружил "речь" (шум микрофона?) → перешёл в VoiceActive → **9 секунд тишины** → timeout → пустой результат!

**9 секунд тишины** после "Voice started" = **VAD ошибся**, речи не было!

---

## 🔧 Что исправлено:

### 1. Увеличен silence_threshold
```rust
// БЫЛО: 1.5 секунды
// СТАЛО: 3.0 секунды - даём Vosk время на распознавание
let silence_threshold: u32 = ((3.0 * sample_rate as f32) / frame_length as f32) as u32;
```

### 2. Добавлено логирование STT
```rust
let stt_result = stt::recognize(&frame_buffer, false);
if let Some(ref text) = stt_result {
    if !text.trim().is_empty() {
        info!("STT recognized during VoiceActive: '{}'", text);
    }
}
```

### 3. Добавлено логирование finish_speech()
```rust
if !final_text.trim().is_empty() {
    // ...
} else {
    warn!("finish_speech() returned empty string - VAD false positive or no speech detected");
}
```

---

## 📋 Инструкция по тестированию:

### Шаг 1: Дождаться сборки
```bash
./rebuild.sh --fast
```

### Шаг 2: Запустить Jarvis
```bash
./jarvis.sh
```

### Шаг 3: Открыть логи в ОДНОМ терминале
```bash
tail -f ~/.config/com.priler.jarvis/app.log
```

### Шаг 4: Сказать команду **БЕЗ wake word** в ДРУГОМ терминале

**Важно:**
- Говори **чётко** и **громко**
- После фразы **замолкни** на 3-4 секунды
- Не говори "джарвис" перед командой!

**Примеры:**
- "открой браузер"
- "какая погода"
- "выключись"

### Шаг 5: Смотреть логи

**Ожидаемые записи (УСПЕХ):**
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] STT recognized during VoiceActive: 'открой браузер'
[INFO] Final STT result after silence: 'открой браузер'
[INFO] finish_speech() returned: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
[INFO] Command executed successfully
```

**Если видишь это (VAD FALSE POSITIVE):**
```
[INFO] VAD: Voice started, flushing X buffered frames
[DEBUG] finish_speech() returned empty string - VAD false positive or no speech detected
[INFO] Final STT result after silence: ''
[DEBUG] VAD: Silence timeout, returning to wait state
```
→ **VAD ошибся** - обнаружил шум вместо речи

**Если видишь это (STT NOT RECOGNIZED):**
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] Final STT result after silence: ''
[DEBUG] finish_speech() returned empty string - VAD false positive or no speech detected
```
→ **Vosk не распознал речь** - говори чётче или проблема с микрофоном

---

## 🐛 Возможные проблемы и решения:

### Проблема 1: VAD false positives (ложные срабатывания)

**Симптомы:**
```
VAD: Voice started, flushing 2 buffered frames
... 9 секунд тишины ...
finish_speech() returned empty string
```

**Причина:** VAD обнаружил шум вместо речи

**Решение:**
1. Проверь микрофон - нет ли шума
2. Попробуй говорить **громче**
3. Проверь настройки VAD (возможно слишком чувствительный)

### Проблема 2: STT не распознаёт

**Симптомы:**
```
VAD: Voice started, flushing XX buffered frames
(нет записей "STT recognized during VoiceActive")
finish_speech() returned empty string
```

**Причина:** Vosk не получает аудио или не распознаёт

**Решение:**
1. Проверь микрофон: `arecord -l`
2. Проверь что микрофон активен: `pactl list sources short`
3. Говори **чётче** и **медленнее**

### Проблема 3: Команда не найдена

**Симптомы:**
```
STT recognized during VoiceActive: 'открой браузер'
finish_speech() returned: 'открой браузер'
No matching no-wake-word command found for: 'открой браузер'
```

**Причина:** Команда не помечена как `wake_word_required: false`

**Решение:**
Проверь файлы команд:
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

## 🎯 Критерии успеха:

**Команда работает БЕЗ wake word если в логах есть:**
1. ✅ `VAD: Voice started` - VAD обнаружил речь
2. ✅ `STT recognized during VoiceActive: '...'` - Vosk распознал фразу
3. ✅ `No-wake-word command detected: '...'` - команда найдена
4. ✅ `Command executed successfully` - команда выполнена

**Если хотя бы одного пункта нет** → проблема!

---

## 📞 Следующие шаги:

1. **Собери проект:** `./rebuild.sh --fast`
2. **Запусти:** `./jarvis.sh`
3. **Смотри логи:** `tail -f ~/.config/com.priler.jarvis/app.log`
4. **Скажи команду** без wake word
5. **Пришли логи** сюда - разберёмся что именно происходит!

<promise>DIAGNOSTICS_READY</promise>
