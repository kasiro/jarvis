"""
Тесты для Environment API: wayland, window management, app launching, command execution
"""
import pytest
from pathlib import Path
import sys
import time

# Добавляем parent directory в path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis_api.environment import Environment


class TestEnvironment:
    """Тесты для Environment API"""
    
    def test_environment_init(self):
        """Тест инициализации Environment"""
        env = Environment()
        assert env is not None
        assert env._wayland is None  # Ленивая инициализация
        assert env._wm is None
        assert env._app_manager is None
    
    def test_environment_singleton(self):
        """Тест глобального экземпляра"""
        from jarvis_api.environment import environment
        assert environment is not None
        assert isinstance(environment, Environment)
    
    def test_get_windows(self):
        """Тест получения списка окон"""
        env = Environment()
        windows = env.get_windows()
        
        # Должен вернуть список (может быть пустым если WindowManager не доступен)
        assert isinstance(windows, list)
    
    def test_is_app_running(self):
        """Тест проверки запущенного приложения"""
        env = Environment()
        
        # Проверяем несуществующее приложение
        result = env.is_app_running("nonexistent_app_12345")
        assert result is False
        
        # Если WindowManager не доступен, тоже вернёт False
        assert isinstance(result, bool)
    
    def test_press_super_number_invalid(self):
        """Тест нажатия Super+number с невалидным номером"""
        env = Environment()
        
        # Должно вернуть False если wayland не доступен
        result = env.press_super_number(99)
        assert result is False
    
    def test_switch_to_workspace(self):
        """Тест переключения рабочего стола"""
        env = Environment()
        
        # Должно вернуть False если wayland не доступен
        result = env.switch_to_workspace(1)
        # Результат зависит от доступности wayland/pydotool
        assert isinstance(result, bool)
    
    def test_minimize_all_windows(self):
        """Тест сворачивания всех окон"""
        env = Environment()
        
        result = env.minimize_all_windows()
        # Результат зависит от доступности WindowManager
        assert isinstance(result, bool)
    
    def test_maximize_all_windows(self):
        """Тест разворачивания всех окон"""
        env = Environment()
        
        result = env.maximize_all_windows()
        # Результат зависит от доступности WindowManager
        assert isinstance(result, bool)
    
    def test_launch_app_invalid(self):
        """Тест запуска несуществующего приложения"""
        env = Environment()
        
        result = env.launch_app("nonexistent_app", 1)
        # Должно вернуть сообщение об ошибке
        assert isinstance(result, str)
        assert "❌" in result or "Неизвестное" in result


class TestEnvironmentIntegration:
    """Интеграционные тесты для Environment"""
    
    def test_environment_in_jarvis(self):
        """Тест что environment доступен в jarvis"""
        from jarvis_api import init_jarvis
        
        jarvis = init_jarvis({
            "phrase": "test",
            "language": "ru",
            "slots": {},
            "command_path": "/tmp"
        })
        
        assert hasattr(jarvis, "environment")
        assert jarvis.environment is not None
        assert isinstance(jarvis.environment, Environment)
    
    def test_environment_methods_available(self):
        """Тест что методы environment доступны"""
        from jarvis_api import init_jarvis
        
        jarvis = init_jarvis({
            "phrase": "test",
            "language": "ru",
            "slots": {},
            "command_path": "/tmp"
        })
        
        # Проверяем наличие методов
        assert hasattr(jarvis.environment, "press_super_number")
        assert hasattr(jarvis.environment, "get_windows")
        assert hasattr(jarvis.environment, "minimize_all_windows")
        assert hasattr(jarvis.environment, "maximize_all_windows")
        assert hasattr(jarvis.environment, "switch_to_workspace")
        # exec методы доступны в jarvis.system
        assert hasattr(jarvis.system, "exec")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
