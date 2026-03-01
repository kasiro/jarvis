"""
HTTP API - HTTP запросы: get, post с использованием aiohttp
"""
import asyncio
import aiohttp
from typing import Optional, Dict, Any, List


class HTTP:
    """
    HTTP API для выполнения HTTP запросов
    
    Использует aiohttp для асинхронных запросов
    """
    
    def __init__(self, timeout: int = 30):
        """
        Инициализировать HTTP клиент
        
        Args:
            timeout: Таймаут запросов в секундах
        """
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Получить или создать сессию"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self._session
    
    async def close(self):
        """Закрыть сессию"""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Выполнить GET запрос
        
        Args:
            url: URL
            headers: HTTP заголовки
            params: Query параметры
            
        Returns:
            Dict с ключами: ok, body, status, headers
        """
        try:
            session = await self._get_session()
            
            async with session.get(url, headers=headers, params=params) as response:
                body = await response.text()
                
                return {
                    "ok": response.status == 200,
                    "body": body,
                    "status": response.status,
                    "headers": dict(response.headers)
                }
                
        except asyncio.TimeoutError:
            return {
                "ok": False,
                "body": "",
                "status": 408,
                "error": "Request timed out"
            }
        except Exception as e:
            return {
                "ok": False,
                "body": "",
                "status": 0,
                "error": str(e)
            }
    
    async def post(
        self,
        url: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Выполнить POST запрос
        
        Args:
            url: URL
            data: Form data
            json: JSON data
            headers: HTTP заголовки
            
        Returns:
            Dict с ключами: ok, body, status, headers
        """
        try:
            session = await self._get_session()
            
            async with session.post(url, data=data, json=json, headers=headers) as response:
                body = await response.text()
                
                return {
                    "ok": 200 <= response.status < 300,
                    "body": body,
                    "status": response.status,
                    "headers": dict(response.headers)
                }
                
        except asyncio.TimeoutError:
            return {
                "ok": False,
                "body": "",
                "status": 408,
                "error": "Request timed out"
            }
        except Exception as e:
            return {
                "ok": False,
                "body": "",
                "status": 0,
                "error": str(e)
            }
    
    async def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Выполнить HTTP запрос произвольным методом
        
        Args:
            method: HTTP метод (GET, POST, PUT, DELETE, etc.)
            url: URL
            **kwargs: Дополнительные аргументы для aiohttp
            
        Returns:
            Dict с ключами: ok, body, status, headers
        """
        try:
            session = await self._get_session()
            
            async with session.request(method, url, **kwargs) as response:
                body = await response.text()
                
                return {
                    "ok": 200 <= response.status < 300,
                    "body": body,
                    "status": response.status,
                    "headers": dict(response.headers)
                }
                
        except asyncio.TimeoutError:
            return {
                "ok": False,
                "body": "",
                "status": 408,
                "error": "Request timed out"
            }
        except Exception as e:
            return {
                "ok": False,
                "body": "",
                "status": 0,
                "error": str(e)
            }


# Глобальный экземпляр
http = HTTP()
