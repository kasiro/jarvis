#!/usr/bin/env python3
"""
Jarvis Server - Async RPC Server для Python команд

Запускается через: uv run python -m jarvis_server
Слушает stdin (JSON), выполняет команды, пишет в stdout (JSON)
"""
import sys
import asyncio
import json
import importlib
import logging
from typing import Any, Dict

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='[JarvisServer] %(levelname)s: %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


async def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Обработать запрос от Rust
    
    Request format:
    {
        "id": 123,
        "type": "execute",
        "module": "modes.kid_mode_on",
        "context": {
            "phrase": "детский режим",
            "language": "ru",
            "slots": {},
            "command_path": "/path/to/command"
        }
    }
    """
    request_id = request.get("id", 0)
    request_type = request.get("type", "execute")
    
    # Handle shutdown
    if request_type == "shutdown":
        logger.info("Shutdown requested")
        return {"id": request_id, "type": "shutdown", "success": True}
    
    # Execute command
    if request_type == "execute":
        module_name = request.get("module")
        context = request.get("context", {})
        
        if not module_name:
            return {
                "id": request_id,
                "type": "error",
                "error": "Module name not provided"
            }
        
        try:
            logger.info(f"Executing module: {module_name}")
            
            # Импортируем модуль (кэшируется Python)
            module = importlib.import_module(module_name)
            
            # Проверяем наличие execute функции
            if not hasattr(module, "execute"):
                return {
                    "id": request_id,
                    "type": "error",
                    "error": f"Module {module_name} has no execute function"
                }
            
            execute_func = getattr(module, "execute")
            
            # Выполняем (sync или async)
            if asyncio.iscoroutinefunction(execute_func):
                result = await execute_func(context)
            else:
                result = execute_func(context)
            
            logger.info(f"Module {module_name} executed successfully")
            
            return {
                "id": request_id,
                "type": "result",
                "success": True,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error executing {module_name}: {e}", exc_info=True)
            return {
                "id": request_id,
                "type": "error",
                "success": False,
                "error": str(e)
            }
    
    return {
        "id": request_id,
        "type": "error",
        "error": f"Unknown request type: {request_type}"
    }


async def main():
    """Main async loop - читает stdin, пишет в stdout"""
    logger.info("Jarvis Server starting...")
    logger.info(f"Python version: {sys.version}")
    
    # Создаём StreamReader для stdin
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    
    # Подключаем stdin к asyncio
    loop = asyncio.get_event_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    
    logger.info("Listening for requests on stdin...")

    try:
        while True:
            # Читаем линию (JSON + newline)
            line = await reader.readline()

            if not line:
                logger.info("EOF received, shutting down")
                break

            try:
                # Распаковываем JSON
                request = json.loads(line.decode('utf-8'))

                # Обрабатываем запрос
                response = await handle_request(request)

                # Упаковываем ответ и пишем в stdout
                sys.stdout.write(json.dumps(response) + '\n')
                sys.stdout.flush()

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                error_response = {
                    "id": 0,
                    "type": "error",
                    "error": f"Invalid JSON: {str(e)}"
                }
                sys.stdout.write(json.dumps(error_response) + '\n')
                sys.stdout.flush()

    except KeyboardInterrupt:
        logger.info("Interrupted, shutting down")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)

    logger.info("Jarvis Server stopped")


if __name__ == "__main__":
    asyncio.run(main())
