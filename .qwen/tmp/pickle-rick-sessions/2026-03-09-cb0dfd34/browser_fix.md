# 🔍 Диагностика: "открой браузер" не сработала

## Проблема по логам:

```
14:00:14.479 - VAD: Voice started, flushing 123 buffered frames
14:00:17.729 - STT recognized: 'открой браузер'
14:00:47.959 - STT recognized: 'нас кушать зовут месте'  ← ЧЕРЕЗ 30 СЕКУНД!
```

**Проблема:** После "открой браузер" **не было silence timeout**! VAD продолжал слушать 30 секунд!

---

## 🔧 Диагноз:

**VAD обнаруживал "речь" постоянно** (шум микрофона?) → `silence_frames` сбрасывался в 0 → timeout никогда не наступал!

---

## ✅ Что исправлено:

### Добавлено логирование VAD:

```rust
// Log every 50 frames (~1 second) to avoid spam
if silence_frames % 50 == 0 {
    let silence_secs = (silence_frames as f32 * frame_length as f32) / sample_rate as f32;
    debug!("VAD: Silence for {} frames ({:.1}s)", silence_frames, silence_secs);
}
```

---

## 📋 Инструкция по тестированию:

### Шаг 1: Собрать проект
```bash
./post_build.sh --profile dev
```

### Шаг 2: Запустить Jarvis
```bash
./jarvis.sh
```

### Шаг 3: Открыть логи
```bash
tail -f ~/.config/com.priler.jarvis/app.log
```

### Шаг 4: Сказать "открой браузер" **без wake word**

**Важно:**
- Говори **чётко** и **громко**
- После фразы **замолкни полностью** на 4-5 секунд
- Не говори ничего после команды!

### Шаг 5: Проверить логи

**ОЖИДАЕМЫЕ ЛОГИ (УСПЕХ):**
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] STT recognized during VoiceActive: 'открой браузер'
[DEBUG] VAD: Silence for 50 frames (1.6s)  ← Логи тишины
[DEBUG] VAD: Silence for 100 frames (3.2s)
[INFO] Final STT result after silence: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
[INFO] Command executed successfully
```

**ЕСЛИ ВИДИШЬ ЭТО (VAD ШУМИТ):**
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] STT recognized during VoiceActive: 'открой браузер'
[DEBUG] VAD: Voice detected, resetting silence counter (total frames: 0)  ← VAD обнаружил шум!
[DEBUG] VAD: Voice detected, resetting silence counter (total frames: 0)  ← Сброс!
[DEBUG] VAD: Voice detected, resetting silence counter (total frames: 0)
```
→ **VAD обнаруживает шум** вместо тишины → timeout не наступает

**ЕСЛИ ВИДИШЬ ЭТО (ВСЁ РАБОТАЕТ):**
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] STT recognized during VoiceActive: 'открой браузер'
[DEBUG] VAD: Silence frame 1/94  ← Тишина пошла
[DEBUG] VAD: Silence frame 2/94
[DEBUG] VAD: Silence frame 3/94
...
[DEBUG] VAD: Silence for 50 frames (1.6s)  ← 1.6 секунды тишины
[DEBUG] VAD: Silence for 100 frames (3.2s)  ← 3.2 секунды тишины
[INFO] Final STT result after silence: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
```

---

## 🐛 Возможные проблемы:

### Проблема 1: VAD обнаруживает шум

**Симптомы:**
```
[DEBUG] VAD: Voice detected, resetting silence counter (total frames: 0)
[DEBUG] VAD: Voice detected, resetting silence counter (total frames: 0)
```

**Причина:** Микрофон ловит фоновый шум

**Решение:**
1. Проверь что вокруг тихо
2. Проверь настройки микрофона
3. Возможно VAD слишком чувствительный

### Проблема 2: STT не распознаёт

**Симптомы:**
```
[INFO] VAD: Voice started, flushing XX buffered frames
(нет записи "STT recognized")
```

**Причина:** Vosk не распознал речь

**Решение:**
- Говори чётче и громче
- Проверь микрофон

### Проблема 3: Команда не найдена

**Симптомы:**
```
[INFO] STT recognized: 'открой браузер'
[INFO] Final STT result after silence: 'открой браузер'
[DEBUG] No matching no-wake-word command found for: 'открой браузер'
```

**Причина:** Команда не помечена как `wake_word_required: false`

**Решение:**
```bash
grep -r "wake_word_required" resources/commands/browser/
```

Ожидаемый результат:
```
resources/commands/browser/command.toml:wake_word_required = false
```

---

## 🎯 Критерии успеха:

**Команда "открой браузер" работает если в логах есть:**
1. ✅ `VAD: Voice started` - VAD обнаружил речь
2. ✅ `STT recognized during VoiceActive: 'открой браузер'` - Vosk распознал
3. ✅ `VAD: Silence for X frames` - пошла тишина
4. ✅ `Final STT result after silence: 'открой браузер'` - фраза сохранена
5. ✅ `No-wake-word command detected: 'открой браузер'` - команда найдена
6. ✅ `Command executed successfully` - браузер открыт!

**Если хотя бы одного пункта нет** → проблема!

---

## 📞 Что делать если не работает:

1. **Собери проект:** `./post_build.sh --profile dev`
2. **Запусти:** `./jarvis.sh`
3. **Смотри логи:** `tail -f ~/.config/com.priler.jarvis/app.log`
4. **Скажи "открой браузер"** без wake word
5. **Замолкни на 5 секунд**
6. **Пришли логи** - разберёмся!

<promise>DIAGNOSTICS_UPDATED</promise>
