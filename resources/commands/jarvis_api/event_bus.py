# core/event_bus.py
import asyncio
from typing import Dict, Any, Callable, Awaitable, List, Optional
import logging

logger = logging.getLogger(__name__)

class EventBus:
    """
    Простая асинхронная шина событий с хранилищем состояний.
    Позволяет подписываться на события и получать уведомления.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self._context: Dict[str, Any] = {}  # текущее состояние

    # ----- Управление подписками -----
    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]):
        """Подписаться на событие. callback будет вызван с данными события."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Подписка на {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable):
        """Отписаться от события."""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            logger.debug(f"Отписка от {event_type}")

    # ----- Публикация событий -----
    async def publish(self, event_type: str, data: Dict[str, Any]):
        """
        Опубликовать событие. Все подписчики будут вызваны асинхронно.
        """
        if data is None:
            data = {}
        logger.info(f"Событие: {event_type} {data}")
        if event_type in self._subscribers:
            # Запускаем все колбэки конкурентно
            await asyncio.gather(
                *[cb(data) for cb in self._subscribers[event_type]],
                return_exceptions=True
            )

    # ----- Работа с состоянием (context) -----
    def set_state(self, key: str, value: Any, publish: bool = True):
        """Установить значение в состоянии. Опционально публикует событие 'state_changed'."""
        old = self._context.get(key)
        self._context[key] = value
        if publish and old != value:
            # Создаём событие об изменении конкретного ключа
            asyncio.create_task(self.publish(f"state:{key}", {"old": old, "new": value}))
            # Также публикуем общее событие изменения состояния
            asyncio.create_task(self.publish("state_changed", {"key": key, "old": old, "new": value}))

    def get_state(self, key: str):
        """Получить значение из состояния."""
        return self._context.get(key)

    def get_all_state(self):
        """Вернуть копию всего состояния."""
        return self._context.copy()

# Глобальный экземпляр шины (синглтон)
_bus: Optional[EventBus] = None

def get_bus() -> EventBus:
    """Получить глобальную шину событий (создаёт при первом вызове)."""
    global _bus
    if _bus is None:
        _bus = EventBus()
    return _bus
