# Product Guidelines

## Voice & Tone

### Core Personality
- **Direct & Concise**: Минимум текста, максимум информации
- **Professional but Approachable**: Технически грамотный, но дружелюбный
- **Confident**: Уверенный в ответах, без извинений за ограничения

### Communication Style
- **Russian First**: Основной язык интерфейса - русский
- **Technical Precision**: Точные формулировки для технических терминов
- **No Fluff**: Никакого "AI Slop" - только существенная информация

## Design Principles

### Visual Identity
- **Minimalist**: Чистый интерфейс без лишних элементов
- **Functional**: Каждая кнопка имеет назначение
- **Consistent**: Единый стиль во всех компонентах

### UX Guidelines
1. **Offline-First**: Все функции работают без интернета
2. **Privacy-First**: Никакой телеметрии, никаких облаков
3. **Transparency**: Пользователь всегда понимает, что происходит
4. **Responsiveness**: Мгновенная обратная связь на действия

## User Experience Principles

### Voice Interaction
- **Wake Word Sensitivity**: Баланс между ложными срабатываниями и пропуском команд
- **Command Feedback**: Звуковое подтверждение распознавания команды
- **Error Handling**: Грамотная обработка нераспознанных команд

### System Integration
- **Native Feel**: Приложение должно ощущаться как часть ОС
- **Resource Efficiency**: Минимальное потребление CPU/RAM в фоне
- **Wayland Compatibility**: Полная поддержка GNOME Wayland

## Code Quality Standards

### Rust Code
- **Safety First**: Никакого `unsafe` без крайней необходимости
- **Zero Warnings**: Сборка без предупреждений
- **Documentation**: Doc comments для публичных API

### Lua Scripts (Commands)
- **Simplicity**: Одна команда = одна задача
- **Error Handling**: Graceful degradation при ошибках
- **Logging**: Структурированное логирование через `jarvis.log()`

### Frontend (Svelte/Vite)
- **TypeScript Strict**: Строгая типизация
- **Component Reusability**: DRY принцип для UI компонентов
- **Performance**: Lazy loading, code splitting

## Testing Requirements

### Coverage Targets
- **Core Logic**: >80% тестовое покрытие
- **Commands**: Integration tests для каждой команды
- **UI**: E2E тесты для критических путей

### Manual Testing
- **Linux CachyOS**: Primary target
- **Windows**: Secondary target (совместимость)
- **Wayland**: Обязательное тестирование на Wayland

## Release Guidelines

### Version Numbering
- Формат: `MAJOR.MINOR.PATCH`
- `MAJOR`: Breaking changes в API команд
- `MINOR`: Новые функции, обратная совместимость
- `PATCH`: Исправления багов

### Release Checklist
- [ ] Все тесты проходят
- [ ] Сборка на Linux работает
- [ ] Сборка на Windows работает (если применимо)
- [ ] Документация обновлена
- [ ] CHANGELOG.md обновлен

## Security & Privacy

### Data Handling
- **No Cloud**: Все данные локально
- **No Telemetry**: Никакой скрытой отправки данных
- **Transparent Storage**: Пользователь знает, где хранятся данные

### System Access
- **Minimal Permissions**: Запрос только необходимых разрешений
- **User Control**: Пользователь контролирует доступ к микрофону, файлам

## Localization

### Language Support
- **Russian**: Primary language (полная поддержка)
- **Ukrainian**: Planned
- **English**: Planned

### Localization Principles
- **UTF-8**: Полная поддержка Unicode
- **Locale-Aware**: Корректная обработка числовых форматов
- **No Hardcoded Strings**: Все строки во fluent-файлах

## Performance Targets

### Startup Time
- **Cold Start**: <2 секунд до готовности
- **Warm Start**: <1 секунды

### Runtime
- **Idle CPU**: <1% в режиме ожидания
- **Memory**: <200MB в фоне
- **Voice Recognition**: <500ms от команды до реакции

## Accessibility

### Visual
- **High Contrast**: Поддержка тем высокой контрастности
- **Scalable UI**: Масштабирование интерфейса

### Audio
- **Visual Feedback**: Дублирование аудио уведомлений визуально
- **Volume Control**: Регулировка громкости ответов

---

## Enforcement

Эти guidelines применяются ко всем новым функциям и исправлениям. Отклонения должны быть обоснованы в PR description.

**Last Updated**: 2026-02-23  
**Maintained By**: Pickle Rick
