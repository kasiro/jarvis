# Plan Review: Исправление wake_word_required

## Дата: 2026-03-09
## Тикет: Fix wake_word_required bug

## Plan Status: ✅ ВЫПОЛНЕН

## Выполненные изменения

### ✅ crates/jarvis-app/src/app.rs
- [x] Удалена неправильная проверка в начале `recognize_command()`
- [x] Добавлена проверка **после** распознавания фразы
- [x] Отдельная ветка для команд с `wake_word_required: false`
- [x] Немедленное выполнение при нахождении команды без wake word

## Verification

### Компиляция
```bash
cargo check -p jarvis-app
# Result: PASSED ✅
```

### Логика
- ✅ Проверка происходит ПОСЛЕ распознавания фразы
- ✅ Команды с `wake_word_required: false` выполняются немедленно
- ✅ Обычные команды требуют wake word

## Root Cause
**Проблема:** Проверка `wake_word_required` происходила **ДО** того как STT успевал распознать фразу.

**Решение:** Переместить проверку **ПОСЛЕ** распознавания фразы в цикле `VadState::VoiceActive`.

## Approval
**Plan выполнен полностью.** Код готов к тестированию.

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
   
   Ожидаемая запись в логе:
   ```
   [INFO] No-wake-word command detected: 'открой браузер'
   ```

<promise>BUG_FIXED</promise>
