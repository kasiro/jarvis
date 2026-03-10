# Диагностика: wake_word_required не срабатывает

## Дата: 2026-03-09
## Проблема: Команда не срабатывает когда говоришь без wake word через время

## Выявленные проблемы

### Проблема #1: Слишком маленький silence_threshold

**Было:**
```rust
let silence_threshold: u32 = ((1.5 * sample_rate as f32) / frame_length as f32) as u32;
// 1.5 секунды
```

**Проблема:**
- Пользователь говорит фразу (2 секунды)
- Тишина 1.5 секунды → timeout
- **Vosk ещё не распознал фразу!**
- `finish_speech()` возвращает пустоту

**Решение:**
```rust
let silence_threshold: u32 = ((3.0 * sample_rate as f32) / frame_length as f32) as u32;
// 3 секунды - даём Vosk время на распознавание
```

### Проблема #2: Недостаточное логирование

**Было:**
- `finish_speech()` молча возвращал результат
- Невозможно понять что именно вернул Vosk

**Решение:**
Добавлено логирование в `finish_speech()`:
```rust
if let Some(ref text) = result {
    if !text.trim().is_empty() {
        info!("finish_speech() returned: '{}'", text);
    } else {
        debug!("finish_speech() returned empty string");
    }
} else {
    debug!("finish_speech() returned None");
}
```

## Выполненные изменения

### 1. crates/jarvis-app/src/app.rs
- Увеличен `silence_threshold` с 1.5 до 3.0 секунд
- Дано время Vosk на распознавание фразы

### 2. crates/jarvis-core/src/stt/vosk.rs
- Добавлено логирование в `finish_speech()`
- Теперь видно что именно возвращает Vosk

## Verification

### Компиляция
```bash
cargo check -p jarvis-core -p jarvis-app
# Result: PASSED ✅
```

## Diagnostic Instructions

### Шаг 1: Собрать проект
```bash
./rebuild.sh --fast
```

### Шаг 2: Запустить Jarvis
```bash
./jarvis.sh
```

### Шаг 3: Включить логирование
```bash
tail -f ~/.config/com.priler.jarvis/app.log
```

### Шаг 4: Протестировать команды без wake word

Сказать **без wake word**:
- "открой браузер"
- "какая погода"
- "выключись"

**Подождать 3-4 секунды** после фразы!

### Шаг 5: Проверить логи

**Ожидаемые записи:**
```
[INFO] VAD: Voice started, flushing XX buffered frames
[INFO] Final STT result after silence: 'открой браузер'
[INFO] finish_speech() returned: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
[INFO] Processing text command: открой браузер
[INFO] Command found: "/path/to/browser"
[INFO] Command executed successfully
```

**Если видишь это:**
```
[DEBUG] finish_speech() returned None
```
→ Vosk не распознал фразу (слишком быстро сказал или шум)

**Если видишь это:**
```
[DEBUG] finish_speech() returned empty string
```
→ Vosk распознал пустоту (проблема с микрофоном или тишина)

**Если видишь это:**
```
[INFO] Final STT result after silence: 'открой браузер'
[INFO] No-wake-word command detected: 'открой браузер'
```
→ **ВСЁ РАБОТАЕТ!** ✅

## Возможные проблемы

### Проблема: finish_speech() возвращает None

**Причины:**
1. **Слишком быстро сказал** - Vosk не успел распознать
2. **Шум в микрофоне** - VAD не обнаружил речь
3. **Проблема с Vosk** - модель не загружена

**Решение:**
- Говори **чётко** и **медленнее**
- Проверь микрофон
- Проверь логи Vosk

### Проблема: finish_speech() возвращает пустую строку

**Причины:**
1. **Тишина** - ничего не сказал
2. **Микрофон не работает**
3. **Vosk не инициализирован**

**Решение:**
- Проверь `arecord -l` - видит ли систему микрофон
- Проверь `pactl list sources short` - активен ли микрофон

### Проблема: Команда найдена но не выполнена

**Причины:**
1. **Ошибка в скрипте** команды
2. **Нет прав** на выполнение

**Решение:**
- Проверь логи выполнения команды
- Проверь права на скрипт

## Рекомендации

1. **Говори чётко** - не бормочи
2. **Делай паузу** после фразы (2-3 секунды)
3. **Смотри логи** - там вся информация
4. **Проверь микрофон** - без него никак

<promise>DIAGNOSTICS_COMPLETE</promise>
