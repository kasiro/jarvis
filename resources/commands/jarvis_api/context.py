"""
Context API - Доступ к контексту команды: phrase, language, slots
"""

from typing import Any, Dict, Optional


class Context:
    """
    Context API для доступа к контексту команды

    Предоставляет доступ к:
    - phrase: распознанная фраза
    - language: язык ("ru"|"en")
    - slots: извлечённые слоты
    """

    def __init__(self, context_data: Optional[Dict[str, Any]] = None):
        """
        Инициализировать Context

        Args:
            context_data: Данные контекста от Rust
        """
        self._data = context_data or {}

    def update(self, context_data: Dict[str, Any]):
        """
        Обновить контекст

        Args:
            context_data: Новые данные контекста
        """
        self._data = context_data

    @property
    def phrase(self) -> str:
        """
        Распознанная фраза

        Returns:
            Фраза или пустая строка
        """
        return self._data.get("phrase", "")

    @property
    def language(self) -> str:
        """
        Язык команды

        Returns:
            "ru" или "en"
        """
        return self._data.get("language", "ru")

    @property
    def slots(self) -> Dict[str, Any]:
        """
        Извлечённые слоты

        Returns:
            Dict со слотами
        """
        return self._data.get("slots", {})

    def get(self, key: str, default: Any = None) -> Any:
        """
        Получить значение из контекста

        Args:
            key: Ключ
            default: Значение по умолчанию

        Returns:
            Значение или default
        """
        return self._data.get(key, default)

    def get_slot(self, slot_name: str, default: Any = None) -> Any:
        """
        Получить значение слота

        Args:
            slot_name: Имя слота
            default: Значение по умолчанию

        Returns:
            Значение слота или default
        """
        return self.slots.get(slot_name, default)

    def has_slot(self, slot_name: str) -> bool:
        """
        Проверить наличие слота

        Args:
            slot_name: Имя слота

        Returns:
            True если слот существует
        """
        return slot_name in self.slots

    def to_dict(self) -> Dict[str, Any]:
        """
        Получить весь контекст как dict

        Returns:
            Копия контекста
        """
        return self._data.copy()


# Глобальный экземпляр (будет инициализирован с контекстом)
context: Optional[Context] = None


def init_context(context_data: Dict[str, Any]) -> Context:
    """Инициализировать глобальный context экземпляр"""
    global context
    context = Context(context_data)
    return context


def get_context() -> Context:
    """Получить глобальный context экземпляр"""
    global context
    if context is None:
        context = Context()
    return context
