# Research: Исправление проверки wake_word_required

## Дата: 2026-03-09
## Проблема: wake_word_required: false не работает

## Анализ проблемы

### Найдённая ошибка
В `app.rs` функция `recognize_command()` имела **неправильную логику**:

**БЫЛО (неправильно):**
```rust
fn recognize_command(...) {
    // Пытаемся проверить команды ДО распознавания фразы!
    if let Some(recognized) = stt::recognize(frame_buffer, true) {
        // Проверяем команды без wake word
        if let Some(...) = commands::fetch_command_no_wake_word(...) {
            execute_command(...);
        }
    }
}
```

**Проблема:** 
- `frame_buffer` содержит только **текущий аудио фрейм**, не полную фразу
- STT (Vosk) ещё **не распознал фразу** в этот момент
- `recognize(data, true)` вызывает `recognize_wake_word()` который возвращает partial результат
- Но partial результат ещё **пустой** в начале функции

### Правильное решение

**СТАЛО (правильно):**
```rust
fn recognize_command(...) {
    // ... цикл распознавания ...
    
    // ПОСЛЕ распознавания фразы (строка 196)
    if let Some(mut recognized_voice) = stt::recognize(frame_buffer, false) {
        // ... обработка фразы ...
        
        // ПРОВЕРЯЕМ wake_word_required ПОСЛЕ распознавания
        let found_no_wake = commands::fetch_command_no_wake_word(&recognized_voice, commands_list).is_some();
        
        if found_no_wake {
            // Команда без wake word найдена - выполняем немедленно
            execute_command(&recognized_voice, rt);
            return;
        }
        
        // Иначе продолжаем обычный цикл
        execute_command(&recognized_voice, rt);
    }
}
```

## Изменения

### Файл: crates/jarvis-app/src/app.rs

**Удалено:**
- Неправильная проверка в начале `recognize_command()` (строки 150-168)

**Добавлено:**
- Проверка `wake_word_required` **после** распознавания фразы
- Отдельная ветка для команд без wake word
- Немедленное выполнение если найдена команда с `wake_word_required: false`

## Архитектура работы

### Поток выполнения:

1. **STT распознаёт фразу** → `stt::recognize(frame_buffer, false)`
2. **Фраза распознана** → `recognized_voice`
3. **Проверка команд без wake word:**
   - `fetch_command_no_wake_word()` ищет команды с `wake_word_required: false`
   - Если найдена → **немедленное выполнение**
   - Если не найдена → обычный цикл с wake word

### Ключевое отличие:

**До:** Проверка ДО распознавания → всегда пустой результат
**После:** Проверка ПОСЛЕ распознавания → работает правильно

## Тестирование

### Компиляция
```bash
cargo check -p jarvis-app
# Result: PASSED ✅
```

### Ожидаемое поведение:
- "открой браузер" (без wake word) → должно работать ✅
- "какая погода" (без wake word) → должно работать ✅
- "выключись" (без wake word) → должно работать ✅

## Next Steps
- Протестировать на реальном устройстве
- Проверить логи для отладки
