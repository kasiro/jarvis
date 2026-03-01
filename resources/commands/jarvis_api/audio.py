"""
Audio API - Воспроизведение звуков: play, play_ok, play_error
"""
import sys
import subprocess
import random
from pathlib import Path
from typing import Optional, List


class Audio:
    """
    Audio API для воспроизведения звуков
    
    Интегрируется с voices модулем Jarvis через Rust
    """
    
    def __init__(self):
        self.sound_dir = self._find_sound_dir()
    
    def _find_sound_dir(self) -> Optional[Path]:
        """Найти директорию со звуками"""
        # Ищем относительно текущей директории
        possible_paths = [
            Path(__file__).parent.parent.parent / "sound" / "voices",
            Path(__file__).parent.parent / "sound" / "voices",
            Path("/home/kasiro/Документы/jarvis/resources/sound/voices"),
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def _get_sound_path(self, sound_name: str, lang: str = "ru") -> Optional[Path]:
        """
        Получить путь к звуковому файлу
        
        Args:
            sound_name: Имя звука (без расширения)
            lang: Язык (ru/en)
            
        Returns:
            Путь к файлу или None
        """
        if not self.sound_dir:
            return None
        
        # Ищем в директории языка
        lang_dir = self.sound_dir / lang
        if lang_dir.exists():
            # Пробуем разные расширения
            for ext in [".mp3", ".wav", ".ogg"]:
                sound_file = lang_dir / f"{sound_name}{ext}"
                if sound_file.exists():
                    return sound_file
        
        # Ищем в корневой директории звуков
        for ext in [".mp3", ".wav", ".ogg"]:
            sound_file = self.sound_dir / f"{sound_name}{ext}"
            if sound_file.exists():
                return sound_file
        
        return None
    
    def _play_file(self, sound_path: Path) -> bool:
        """
        Воспроизвести звуковой файл
        
        Args:
            sound_path: Путь к файлу
            
        Returns:
            True если успешно
        """
        try:
            # Определяем платформу и используем соответствующий плеер
            if sys.platform.startswith("linux"):
                # Пробуем разные плееры
                players = [
                    ["paplay", str(sound_path)],  # PulseAudio
                    ["aplay", str(sound_path)],   # ALSA
                    ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(sound_path)],  # FFmpeg
                ]
                
                for player_cmd in players:
                    try:
                        subprocess.run(
                            player_cmd,
                            capture_output=True,
                            timeout=30
                        )
                        return True
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        continue
                
            elif sys.platform.startswith("darwin"):
                # macOS: afplay
                subprocess.run(
                    ["afplay", str(sound_path)],
                    capture_output=True,
                    timeout=30
                )
                return True
                
            elif sys.platform.startswith("win"):
                # Windows: PowerShell
                script = f"""
                Add-Type -AssemblyName System.Speech
                $player = New-Object System.Media.SoundPlayer
                $player.SoundLocation = '{sound_path}'
                $player.PlaySync()
                """
                subprocess.run(
                    ["powershell", "-Command", script],
                    capture_output=True,
                    timeout=30
                )
                return True
            
            return False
            
        except Exception as e:
            print(f"[Jarvis:AUDIO] Failed to play {sound_path}: {e}", file=sys.stderr)
            return False
    
    def play(self, sound_name: str, lang: str = "ru") -> bool:
        """
        Воспроизвести конкретный звук
        
        Args:
            sound_name: Имя звука (например, "ok1")
            lang: Язык (ru/en)
            
        Returns:
            True если успешно
        """
        sound_path = self._get_sound_path(sound_name, lang)
        
        if not sound_path:
            print(f"[Jarvis:AUDIO] Sound not found: {sound_name}", file=sys.stderr)
            return False
        
        return self._play_file(sound_path)
    
    def play_ok(self) -> bool:
        """
        Воспроизвести случайный OK звук
        
        Returns:
            True если успешно
        """
        ok_sounds = ["ok1", "ok2", "ok3"]
        sound_name = random.choice(ok_sounds)
        return self.play(sound_name)
    
    def play_error(self) -> bool:
        """
        Воспроизвести звук ошибки
        
        Returns:
            True если успешно
        """
        return self.play("error")
    
    def play_random(self, sounds: List[str], lang: str = "ru") -> bool:
        """
        Воспроизвести случайный звук из списка
        
        Args:
            sounds: Список имён звуков
            lang: Язык
            
        Returns:
            True если успешно
        """
        if not sounds:
            return False
        
        sound_name = random.choice(sounds)
        return self.play(sound_name, lang)


# Глобальный экземпляр
audio = Audio()
