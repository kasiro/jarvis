"""
Environment API - Управление окружением Wayland и окнами

Интеграция с wayland.py и wm_manager.py
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any

# Добавляем parent directory в path для импорта wayland и wm_manager
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


class Environment:
    """
    Environment API для управления окружением Wayland и окнами
    """
    
    def __init__(self):
        self._wayland = None
        self._wm = None
        self._app_manager = None
    
    def _init_wayland(self):
        """Ленивая инициализация WaylandController"""
        if self._wayland is None:
            try:
                from wayland import WaylandController
                self._wayland = WaylandController()
            except ImportError as e:
                print(f"[Jarvis:ENV] Failed to import WaylandController: {e}", file=sys.stderr)
                return None
        return self._wayland
    
    def _init_window_manager(self):
        """Ленивая инициализация WindowManager"""
        if self._wm is None:
            try:
                from wm_manager import WindowManager
                self._wm = WindowManager()
            except ImportError as e:
                print(f"[Jarvis:ENV] Failed to import WindowManager: {e}", file=sys.stderr)
                return None
        return self._wm
    
    def _init_app_manager(self):
        """Ленивая инициализация AppManager"""
        if self._app_manager is None:
            try:
                from wm_manager import AppManager
                self._app_manager = AppManager()
            except ImportError as e:
                print(f"[Jarvis:ENV] Failed to import AppManager: {e}", file=sys.stderr)
                return None
        return self._app_manager
    
    # ===== Wayland Control =====
    
    def press_super_number(self, number: int) -> bool:
        """
        Нажать комбинацию Super + цифра
        
        Args:
            number: Цифра от 1 до 4
            
        Returns:
            True если успешно
        """
        wayland = self._init_wayland()
        if not wayland:
            return False
        
        try:
            wayland.press_super_number(number)
            return True
        except Exception as e:
            print(f"[Jarvis:ENV] Error pressing Super+{number}: {e}", file=sys.stderr)
            return False
    
    # ===== Window Management =====
    
    def get_windows(self) -> List[Dict]:
        """
        Получить список всех окон
        
        Returns:
            Список словарей с информацией об окнах
        """
        wm = self._init_window_manager()
        if not wm:
            return []
        
        return wm.get_windows()
    
    def minimize_all_windows(self) -> bool:
        """
        Свернуть все окна
        
        Returns:
            True если успешно
        """
        wm = self._init_window_manager()
        if not wm:
            return False
        
        return wm._minimize_all_manually()
    
    def maximize_all_windows(self) -> bool:
        """
        Развернуть все окна
        
        Returns:
            True если успешно
        """
        wm = self._init_window_manager()
        if not wm:
            return False
        
        return wm._maximize_all_manually()
    
    def is_app_running(self, wm_class: str) -> bool:
        """
        Проверить, запущено ли приложение
        
        Args:
            wm_class: WM класс приложения (например, "zen-browser")
            
        Returns:
            True если приложение запущено
        """
        wm = self._init_window_manager()
        if not wm:
            return False
        
        return wm.is_running(wm_class)
    
    def move_window_to_workspace(self, window_id: int, workspace: int) -> bool:
        """
        Переместить окно на рабочий стол
        
        Args:
            window_id: ID окна
            workspace: Номер рабочего стола (0-based)
            
        Returns:
            True если успешно
        """
        wm = self._init_window_manager()
        if not wm:
            return False
        
        return wm.move_to_workspace(window_id, workspace)
    
    # ===== Application Launching =====
    
    def launch_app(self, app_name: str, workspace: int = 1) -> str:
        """
        Запустить приложение на указанном рабочем столе
        
        Args:
            app_name: Имя приложения (zen-browser, zed)
            workspace: Номер рабочего стола (1-based)
            
        Returns:
            Сообщение о результате
        """
        app_mgr = self._init_app_manager()
        if not app_mgr:
            return "❌ AppManager не доступен"
        
        launcher = app_mgr.launcher
        return launcher.launch(app_name, workspace)
    
    def launch_or_move_app(self, app_name: str, wm_class: str, workspace: int):
        """
        Запустить приложение или переключиться на него
        
        Args:
            app_name: Имя приложения
            wm_class: WM класс приложения
            workspace: Номер рабочего стола
        """
        app_mgr = self._init_app_manager()
        if not app_mgr:
            return False
        
        app_mgr.launch_or_move(app_name, wm_class, workspace)
        return True
    
    # ===== Workspace Control =====
    
    def switch_to_workspace(self, number: int) -> bool:
        """
        Переключиться на рабочий стол
        
        Args:
            number: Номер рабочего стола (1-4)
            
        Returns:
            True если успешно
        """
        return self.press_super_number(number)


# Глобальный экземпляр
environment = Environment()
