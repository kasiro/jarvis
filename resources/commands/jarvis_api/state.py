"""
State API - Хранение состояния команды в .state.json
"""
import json
from pathlib import Path
from typing import Any, Optional, List, Dict


class State:
    """
    State Manager для хранения состояния команды
    
    Хранит данные в .state.json в директории команды
    """
    
    def __init__(self, command_path: str = ""):
        """
        Инициализировать State Manager
        
        Args:
            command_path: Путь к директории команды
        """
        self.command_path = Path(command_path) if command_path else Path.cwd()
        self.state_file = self.command_path / ".state.json"
    
    def _load(self) -> Dict[str, Any]:
        """Загрузить состояние из файла"""
        if not self.state_file.exists():
            return {}
        
        try:
            content = self.state_file.read_text(encoding="utf-8")
            return json.loads(content)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _save(self, data: Dict[str, Any]) -> bool:
        """Сохранить состояние в файл"""
        try:
            self.state_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Optional[Any]:
        """
        Получить значение из состояния
        
        Args:
            key: Ключ
            default: Значение по умолчанию
            
        Returns:
            Значение или None если не найдено
        """
        data = self._load()
        return data.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Установить значение в состоянии
        
        Args:
            key: Ключ
            value: Значение
            
        Returns:
            True если успешно
        """
        data = self._load()
        data[key] = value
        return self._save(data)
    
    def delete(self, key: str) -> bool:
        """
        Удалить ключ из состояния
        
        Args:
            key: Ключ для удаления
            
        Returns:
            True если ключ существовал и был удалён
        """
        data = self._load()
        existed = key in data
        if existed:
            del data[key]
            self._save(data)
        return existed
    
    def clear(self) -> bool:
        """
        Очистить всё состояние
        
        Returns:
            True если успешно
        """
        return self._save({})
    
    def keys(self) -> List[str]:
        """
        Получить все ключи
        
        Returns:
            Список ключей
        """
        data = self._load()
        return list(data.keys())
    
    def all(self) -> Dict[str, Any]:
        """
        Получить всё состояние
        
        Returns:
            Копия всего состояния
        """
        return self._load().copy()


# Глобальный экземпляр (будет инициализирован с command_path)
state: Optional[State] = None


def init_state(command_path: str) -> State:
    """Инициализировать глобальный state экземпляр"""
    global state
    state = State(command_path)
    return state


def get_state() -> State:
    """Получить глобальный state экземпляр"""
    global state
    if state is None:
        state = State()
    return state
