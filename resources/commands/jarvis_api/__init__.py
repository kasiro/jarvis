"""
Jarvis API - Python API для команд Jarvis

Использование:
    from jarvis_api import jarvis
    
    async def execute(context):
        jarvis.log("info", "Hello from Python!")
        jarvis.state.set("count", 1)
        jarvis.system.notify("Title", "Message")
"""
from typing import Optional
from .core import log, print_fn as print, sleep, speak
from .state import State, state
from .system import System, system
from .audio import Audio, audio
from .http import HTTP, http
from .context import Context, context
from .modes import Modes, modes
from .environment import Environment, environment


class Jarvis:
    """Главный класс Jarvis API"""
    
    def __init__(self, context: dict = None):
        """
        Инициализировать Jarvis API
        
        Args:
            context: Контекст команды (phrase, language, slots, command_path)
        """
        self._context = context or {}
        
        # Инициализируем API модули с контекстом
        self._state = State(self._context.get("command_path", ""))
        self._system = System()
        self._audio = Audio()
        self._http = HTTP()
        self._context_api = Context(self._context)
        self._modes = Modes(self._context.get("command_path", ""), self._state)  # Передаём state
        self._environment = Environment()
        
        # Экспортируем функции
        self.log = log
        self.print = print  # Уже импортирован как print_fn as print
        self.sleep = sleep
        self.speak = speak
        self.state = self._state
        self.system = self._system
        self.audio = self._audio
        self.http = self._http
        self.context = self._context_api
        self.modes = self._modes
        self.environment = self._environment


# Глобальный экземпляр (будет инициализирован с контекстом в jarvis_server)
_jarvis_instance: Optional[Jarvis] = None


def init_jarvis(context: dict) -> Jarvis:
    """Инициализировать глобальный jarvis экземпляр с контекстом"""
    global _jarvis_instance
    _jarvis_instance = Jarvis(context)
    return _jarvis_instance


def get_jarvis() -> Jarvis:
    """Получить глобальный jarvis экземпляр"""
    global _jarvis_instance
    if _jarvis_instance is None:
        _jarvis_instance = Jarvis({})
    return _jarvis_instance


# Для обратной совместимости
jarvis = get_jarvis()


__all__ = [
    # Основной класс
    "Jarvis",
    "init_jarvis",
    "get_jarvis",
    "jarvis",
    
    # Core API
    "log",
    "print_fn",
    "sleep",
    "speak",
    
    # State API
    "State",
    "state",
    
    # System API
    "System",
    "system",
    
    # Audio API
    "Audio",
    "audio",
    
    # HTTP API
    "HTTP",
    "http",
    
    # Context API
    "Context",
    "context",
    
    # Modes API
    "Modes",
    "modes",
    
    # Environment API
    "Environment",
    "environment",
]
