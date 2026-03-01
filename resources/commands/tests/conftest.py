"""
Pytest конфигурация и fixtures
"""
import pytest
import sys
from pathlib import Path


def pytest_configure(config):
    """Настраивает PYTHON_PATH перед запуском тестов"""
    # Добавляем корневую директорию commands в path
    root_dir = Path(__file__).parent.parent
    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))


@pytest.fixture
def test_context():
    """Создаёт тестовый контекст для команд"""
    return {
        "phrase": "тестовая команда",
        "language": "ru",
        "slots": {},
        "command_path": str(Path(__file__).parent.parent)
    }
