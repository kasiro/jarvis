"""
Тесты для Core API: log, print, sleep, speak
"""
import asyncio
import pytest
from io import StringIO
import sys

from jarvis_api.core import log, print_fn, sleep, speak


class TestLog:
    """Тесты для функции log()"""
    
    def test_log_info(self, capsys):
        """Тест логирования info уровня"""
        log("info", "Test message")
        captured = capsys.readouterr()
        assert "[Jarvis:INFO]" in captured.err
        assert "Test message" in captured.err
    
    def test_log_debug(self, capsys):
        """Тест логирования debug уровня"""
        log("debug", "Debug message")
        captured = capsys.readouterr()
        assert "[Jarvis:DEBUG]" in captured.err
        assert "Debug message" in captured.err
    
    def test_log_warn(self, capsys):
        """Тест логирования warn уровня"""
        log("warn", "Warning message")
        captured = capsys.readouterr()
        assert "[Jarvis:WARN]" in captured.err
        assert "Warning message" in captured.err
    
    def test_log_error(self, capsys):
        """Тест логирования error уровня"""
        log("error", "Error message")
        captured = capsys.readouterr()
        assert "[Jarvis:ERROR]" in captured.err
        assert "Error message" in captured.err
    
    def test_log_unknown_level(self, capsys):
        """Тест логирования с неизвестным уровнем (должен использовать info)"""
        log("unknown", "Unknown level message")
        captured = capsys.readouterr()
        # Неизвестный уровень fallback'ится на info в logger, но print сохраняет оригинальный
        assert "Unknown level message" in captured.err


class TestPrint:
    """Тесты для функции print_fn()"""
    
    def test_print_single_arg(self, capsys):
        """Тест print с одним аргументом"""
        print_fn("Hello")
        captured = capsys.readouterr()
        assert "[Jarvis:PRINT]" in captured.err
        assert "Hello" in captured.err
    
    def test_print_multiple_args(self, capsys):
        """Тест print с несколькими аргументами"""
        print_fn("Value:", 42, "items")
        captured = capsys.readouterr()
        assert "Value: 42 items" in captured.err


class TestSleep:
    """Тесты для функции sleep()"""
    
    @pytest.mark.asyncio
    async def test_sleep_duration(self):
        """Тест продолжительности сна"""
        import time
        
        start = time.time()
        await sleep(100)  # 100ms
        elapsed = time.time() - start
        
        # Должно пройти хотя бы 80ms (с небольшой погрешностью)
        assert elapsed >= 0.08
        assert elapsed < 0.5  # Но не больше 500ms
    
    @pytest.mark.asyncio
    async def test_sleep_zero(self):
        """Тест сна с нулевой продолжительностью"""
        await sleep(0)
        # Должно выполниться без ошибок


class TestSpeak:
    """Тесты для функции speak()"""
    
    def test_speak(self, capsys):
        """Тест TTS функции"""
        speak("Hello World")
        captured = capsys.readouterr()
        assert "[Jarvis:SPEAK]" in captured.err
        assert "Hello World" in captured.err


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
