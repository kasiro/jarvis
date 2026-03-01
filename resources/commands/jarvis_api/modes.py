"""
Modes API - Управление режимами: get_current, set_mode
"""
import sys
import asyncio
from typing import Optional
from pathlib import Path

# Добавляем parent directory в path для импорта mode_manager и event_bus
sys.path.insert(0, str(Path(__file__).parent.parent))


class Modes:
    """
    Modes API для управления режимами Jarvis
    
    Режимы:
    - normal: обычный режим
    - kid: детский режим
    - dev: режим разработчика
    """
    
    VALID_MODES = ["normal", "kid", "dev"]
    
    def __init__(self, command_path: str = "", state: State = None):
        """
        Инициализировать Modes API
        
        Args:
            command_path: Путь к директории команды для state (если state не предоставлен)
            state: State объект для хранения режима
        """
        self.command_path = command_path
        self.state = state  # State объект от Jarvis
        self._manager = None
        self._bus = None
    
    def _get_manager(self):
        """Ленивая инициализация ModesManager"""
        if self._manager is None:
            try:
                # Импортируем ModesManager из jarvis_api
                from .mode_manager import ModesManager
                # Передаём state объект в ModesManager
                self._manager = ModesManager(self.state)
            except ImportError as e:
                print(f"[Jarvis:MODES] Failed to import ModesManager: {e}", file=sys.stderr)
                return None
        return self._manager
    
    def _get_bus(self):
        """Ленивая инициализация EventBus"""
        if self._bus is None:
            try:
                import sys
                from pathlib import Path
                # Добавляем parent directory в path
                parent_dir = str(Path(__file__).parent.parent)
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)
                from event_bus import get_bus
                self._bus = get_bus()
            except ImportError as e:
                print(f"[Jarvis:MODES] Failed to import EventBus: {e}", file=sys.stderr)
                return None
        return self._bus
    
    def get_current(self) -> str:
        """
        Получить текущий режим
        
        Returns:
            "normal", "kid", или "dev"
        """
        manager = self._get_manager()
        
        if manager:
            return manager.get_current_mode()
        
        # Fallback: читаем из state
        try:
            from .state import State  # Относительный импорт внутри jarvis_api
            state = State()
            mode = state.get("mode", "normal")
            return mode if mode in self.VALID_MODES else "normal"
        except Exception:
            return "normal"
    
    async def set_mode(self, new_mode: str) -> bool:
        """
        Установить новый режим
        
        Args:
            new_mode: "normal", "kid", или "dev"
            
        Returns:
            True если успешно
        """
        if new_mode not in self.VALID_MODES:
            print(f"[Jarvis:MODES] Invalid mode: {new_mode}. Valid modes: {self.VALID_MODES}", file=sys.stderr)
            return False
        
        manager = self._get_manager()
        
        if manager:
            try:
                # Используем async метод ModesManager
                if asyncio.iscoroutinefunction(manager.set_mode):
                    success = await manager.set_mode(new_mode)
                else:
                    success = manager.set_mode(new_mode)
                
                if success:
                    print(f"[Jarvis:MODES] Mode set to: {new_mode}", file=sys.stderr)
                else:
                    print(f"[Jarvis:MODES] Failed to set mode: {new_mode}", file=sys.stderr)
                
                return success
                
            except Exception as e:
                print(f"[Jarvis:MODES] Error setting mode: {e}", file=sys.stderr)
                return False
        
        # Fallback: записываем напрямую в state
        try:
            from .state import State
            state = State(self.command_path)
            state.set("mode", new_mode)
            print(f"[Jarvis:MODES] Mode set to: {new_mode} (fallback)", file=sys.stderr)
            return True
        except Exception as e:
            print(f"[Jarvis:MODES] Fallback failed: {e}", file=sys.stderr)
            return False
    
    def is_kid_mode(self) -> bool:
        """
        Проверить, активен ли детский режим
        
        Returns:
            True если kid mode активен
        """
        return self.get_current() == "kid"
    
    def is_dev_mode(self) -> bool:
        """
        Проверить, активен ли режим разработчика
        
        Returns:
            True если dev mode активен
        """
        return self.get_current() == "dev"
    
    def is_normal_mode(self) -> bool:
        """
        Проверить, активен ли обычный режим
        
        Returns:
            True если normal mode активен
        """
        return self.get_current() == "normal"


# Глобальный экземпляр
modes = Modes()
