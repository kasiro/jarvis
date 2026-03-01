"""
Core API - Базовые функции: log, print, sleep, speak
"""
import asyncio
import sys
import logging
from typing import Any

# Настройка логирования
logger = logging.getLogger(__name__)


def log(level: str, message: str) -> None:
    """
    Логировать сообщение
    
    Args:
        level: Уровень логирования (debug, info, warn, error)
        message: Сообщение
    """
    level = level.lower()
    
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warn" or level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    else:
        # Неизвестный уровень - fallback на info
        logger.info(message)
    
    # Также пишем в stderr для Rust
    print(f"[Jarvis:{level.upper()}] {message}", file=sys.stderr)


def print_fn(*args: Any, **kwargs: Any) -> None:
    """
    Print функция (переименована чтобы избежать конфликта с built-in print)
    """
    message = " ".join(str(arg) for arg in args)
    logger.info(message)
    print(f"[Jarvis:PRINT] {message}", file=sys.stderr)


async def sleep(ms: int) -> None:
    """
    Асинхронная задержка
    
    Args:
        ms: Миллисекунды
    """
    seconds = ms / 1000.0
    await asyncio.sleep(seconds)


def speak(text: str) -> None:
    """
    TTS - Text To Speech (заглушка)
    
    Args:
        text: Текст для произнесения
    """
    # TODO: Интеграция с TTS системой
    logger.info(f"[TTS] {text}")
    print(f"[Jarvis:SPEAK] {text}", file=sys.stderr)
