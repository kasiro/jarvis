"""
Тесты для State API: get, set, delete, clear, keys, all
"""
import pytest
import json
from pathlib import Path
import tempfile
import shutil

from jarvis_api.state import State


class TestState:
    """Тесты для State API"""
    
    @pytest.fixture
    def temp_dir(self):
        """Создаёт временную директорию для тестов"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def state(self, temp_dir):
        """Создаёт State с временной директорией"""
        return State(temp_dir)
    
    def test_set_and_get(self, state):
        """Тест установки и получения значения"""
        state.set("key", "value")
        assert state.get("key") == "value"
    
    def test_get_nonexistent(self, state):
        """Тест получения несуществующего ключа"""
        assert state.get("nonexistent") is None
        assert state.get("nonexistent", "default") == "default"
    
    def test_set_overwrite(self, state):
        """Тест перезаписи значения"""
        state.set("key", "value1")
        state.set("key", "value2")
        assert state.get("key") == "value2"
    
    def test_delete(self, state):
        """Тест удаления ключа"""
        state.set("key", "value")
        assert state.delete("key") is True
        assert state.get("key") is None
        assert state.delete("key") is False  # Уже удалён
    
    def test_clear(self, state):
        """Тест очистки всего состояния"""
        state.set("key1", "value1")
        state.set("key2", "value2")
        state.clear()
        assert state.get("key1") is None
        assert state.get("key2") is None
    
    def test_keys(self, state):
        """Тест получения всех ключей"""
        state.set("a", 1)
        state.set("b", 2)
        state.set("c", 3)
        keys = state.keys()
        assert sorted(keys) == ["a", "b", "c"]
    
    def test_all(self, state):
        """Тест получения всего состояния"""
        state.set("a", 1)
        state.set("b", 2)
        all_data = state.all()
        assert all_data == {"a": 1, "b": 2}
    
    def test_all_returns_copy(self, state):
        """Тест что all() возвращает копию"""
        state.set("key", "value")
        all_data = state.all()
        all_data["key"] = "modified"
        assert state.get("key") == "value"  # Оригинал не изменён
    
    def test_persistence(self, temp_dir):
        """Тест сохранения состояния между экземплярами"""
        state1 = State(temp_dir)
        state1.set("key", "value")
        
        # Создаём новый экземпляр с той же директорией
        state2 = State(temp_dir)
        assert state2.get("key") == "value"
    
    def test_json_types(self, state):
        """Тест различных JSON типов"""
        state.set("string", "hello")
        state.set("number", 42)
        state.set("float", 3.14)
        state.set("bool", True)
        state.set("null", None)
        state.set("list", [1, 2, 3])
        state.set("dict", {"nested": "value"})
        
        assert state.get("string") == "hello"
        assert state.get("number") == 42
        assert state.get("float") == 3.14
        assert state.get("bool") is True
        assert state.get("null") is None
        assert state.get("list") == [1, 2, 3]
        assert state.get("dict") == {"nested": "value"}
    
    def test_state_file_location(self, temp_dir):
        """Тест расположения файла состояния"""
        state = State(temp_dir)
        state_file = Path(temp_dir) / ".state.json"
        
        state.set("key", "value")
        assert state_file.exists()
        
        # Проверяем содержимое файла
        content = json.loads(state_file.read_text())
        assert content["key"] == "value"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
