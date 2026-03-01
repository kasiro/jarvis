from .event_bus import get_bus
from .state import State

class ModesManager:
    """Управляет режимами работы ассистента и публикует события об их смене."""

    MODES = ["normal", "kid", "dev"]

    def __init__(self, state: State = None):
        """
        Инициализировать ModesManager
        
        Args:
            state: State объект для хранения режима (опционально)
        """
        self.bus = get_bus()
        self.state = state if state else State()
        self.current_mode = self.state.get("mode") or "normal"

    async def set_mode(self, new_mode: str) -> bool:
        """Переключить режим и оповестить систему."""
        if new_mode not in self.MODES:
            return False

        old_mode = self.current_mode
        if old_mode == new_mode:
            return True

        self.current_mode = new_mode
        
        # Сохраняем в State (который пишет в .state.json)
        self.state.set("mode", new_mode)
        
        # Также публикуем в EventBus
        self.bus.set_state("mode", new_mode, publish=True)

        # Публикуем специальное событие для режима
        await self.bus.publish("mode_changed", {"old": old_mode, "new": new_mode})
        return True

    def get_current_mode(self) -> str:
        return self.current_mode
