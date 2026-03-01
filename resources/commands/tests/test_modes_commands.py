"""
Тесты для Modes команд: kid_mode_on, kid_mode_off, dev_mode_on, check_mode
"""
import asyncio
import pytest
from pathlib import Path
import sys
import tempfile

# Добавляем parent directory в path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestKidModeOn:
    """Тесты для kid_mode_on.py"""
    
    @pytest.mark.asyncio
    async def test_kid_mode_on_execute(self):
        """Тест выполнения kid_mode_on"""
        import tempfile
        from jarvis_api import init_jarvis, get_jarvis
        
        # Создаём временную директорию для state
        with tempfile.TemporaryDirectory() as temp_dir:
            # Инициализируем jarvis с контекстом
            context = {
                "phrase": "детский режим",
                "language": "ru",
                "slots": {},
                "command_path": temp_dir
            }
            jarvis = init_jarvis(context)
            
            from modes.kid_mode_on import execute
            
            # Выполняем команду
            await execute(context)
            
            # Используем тот же state что и jarvis
            assert jarvis.state.get("mode") == "kid"


class TestKidModeOff:
    """Тесты для kid_mode_off.py"""
    
    @pytest.mark.asyncio
    async def test_kid_mode_off_execute(self):
        """Тест выполнения kid_mode_off"""
        from jarvis_api import init_jarvis, get_jarvis
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Инициализируем jarvis с контекстом
            context = {
                "phrase": "обычный режим",
                "language": "ru",
                "slots": {},
                "command_path": temp_dir
            }
            jarvis = init_jarvis(context)
            
            # Сначала устанавливаем kid mode напрямую в state
            jarvis.state.set("mode", "kid")
            
            from modes.kid_mode_off import execute
            
            # Выполняем команду
            await execute(context)
            
            # Проверяем что режим сброшен
            assert jarvis.state.get("mode") == "normal"


class TestDevModeOn:
    """Тесты для dev_mode_on.py"""
    
    @pytest.mark.asyncio
    async def test_dev_mode_on_execute(self):
        """Тест выполнения dev_mode_on"""
        from jarvis_api import init_jarvis
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            context = {
                "phrase": "режим разработчика",
                "language": "ru",
                "slots": {},
                "command_path": temp_dir
            }
            
            jarvis = init_jarvis(context)
            
            from modes.dev_mode_on import execute
            
            # Выполняем команду
            await execute(context)
            
            # Проверяем что режим установлен
            assert jarvis.state.get("mode") == "dev"


class TestCheckMode:
    """Тесты для check_mode.py"""
    
    @pytest.mark.asyncio
    async def test_check_mode_execute(self):
        """Тест выполнения check_mode"""
        from jarvis_api import init_jarvis
        from jarvis_api.state import State
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Устанавливаем режим
            state = State(temp_dir)
            state.set("mode", "kid")
            
            context = {
                "phrase": "какой режим",
                "language": "ru",
                "slots": {},
                "command_path": temp_dir
            }
            
            init_jarvis(context)
            
            from modes.check_mode import execute
            
            # Выполняем команду (должна пройти без ошибок)
            await execute(context)


class TestModesIntegration:
    """Интеграционные тесты для режимов"""
    
    @pytest.mark.asyncio
    async def test_mode_transitions(self):
        """Тест переходов между режимами"""
        from jarvis_api import init_jarvis
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Normal → Kid
            jarvis = init_jarvis({"phrase": "kid", "language": "ru", "slots": {}, "command_path": temp_dir})
            from modes.kid_mode_on import execute as kid_on
            await kid_on({"phrase": "kid", "language": "ru", "slots": {}, "command_path": temp_dir})
            assert jarvis.state.get("mode") == "kid"
            
            # Kid → Dev
            jarvis = init_jarvis({"phrase": "dev", "language": "ru", "slots": {}, "command_path": temp_dir})
            from modes.dev_mode_on import execute as dev_on
            await dev_on({"phrase": "dev", "language": "ru", "slots": {}, "command_path": temp_dir})
            assert jarvis.state.get("mode") == "dev"
            
            # Dev → Normal
            jarvis = init_jarvis({"phrase": "normal", "language": "ru", "slots": {}, "command_path": temp_dir})
            from modes.kid_mode_off import execute as kid_off
            await kid_off({"phrase": "normal", "language": "ru", "slots": {}, "command_path": temp_dir})
            assert jarvis.state.get("mode") == "normal"
    
    @pytest.mark.asyncio
    async def test_invalid_mode(self):
        """Тест установки неверного режима"""
        from jarvis_api.modes import modes
        
        success = await modes.set_mode("invalid_mode")
        assert success is False
    
    @pytest.mark.asyncio
    async def test_get_current_mode(self):
        """Тест получения текущего режима"""
        from jarvis_api.modes import modes
        
        # Просто проверяем что метод работает
        current = modes.get_current()
        assert current in ["normal", "kid", "dev", "unknown"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
