"""
Core API - Базовые функции: log, print, sleep, speak
"""
import asyncio
import os
import sys
import logging
from pathlib import Path
from typing import Any, Optional

# Настройка логирования
logger = logging.getLogger(__name__)

# Глобальные переменные для lazy initialization
_logger_initialized = False
_default_log_path: Optional[str] = None


def _setup_logger(log_file_path: Optional[str] = None) -> None:
    """
    Инициализировать logger с dual output (console + file)

    Args:
        log_file_path: Путь к файлу логов (опционально)
    """
    global _logger_initialized

    if _logger_initialized:
        return

    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Предотвратить дублирование в root logger
    logger.handlers.clear()

    # 1. StreamHandler для console (stderr)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('[Jarvis:%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 2. FileHandler для file (опционально)
    if log_file_path:
        try:
            # Создать директорию если не существует
            log_dir = os.path.dirname(log_file_path)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)

            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s [Jarvis:%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # Fallback: только console если файл недоступен
            logger.warning(f"Failed to setup file logging: {e}", exc_info=True)

    _logger_initialized = True


def log(level: str, message: str) -> None:
    """
    Логировать сообщение

    Args:
        level: Уровень логирования (debug, info, warn, error)
        message: Сообщение
    """
    # Инициализировать logger при первом вызове
    if not _logger_initialized:
        # Получить путь из environment или использовать default
        log_path = os.environ.get('JARVIS_LOG_FILE')
        if not log_path:
            # Default путь: ~/.local/share/jarvis/logs/jarvis_api.log
            home = Path.home()
            log_dir = home / '.local' / 'share' / 'jarvis' / 'logs'
            log_path = str(log_dir / 'jarvis_api.log')
        _setup_logger(log_path)

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


def print_fn(*args: Any, **kwargs: Any) -> None:
    """
    Print функция (переименована чтобы избежать конфликта с built-in print)
    """
    message = " ".join(str(arg) for arg in args)
    logger.info(message)


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
