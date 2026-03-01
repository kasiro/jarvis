import subprocess
import time
import logging

logger = logging.getLogger(__name__)

class VPNController:
    """
    Управление AmneziaVPN через CLI.

    CLI клиент: /usr/bin/AmneziaVPN
    - Запускает GUI процесс который подключается к сервису
    - Сервис создаёт интерфейс tun2 через tun2socks
    """
    def __init__(self, server_index=0, cleanup=False):
        self.executable = '/usr/bin/AmneziaVPN'
        self.interface_name = 'tun2'
        self.server_index = server_index
        # cleanup=False по умолчанию - не убиваем существующие процессы
        if cleanup:
            self._kill_existing_processes()

    def _kill_existing_processes(self):
        """Завершает все процессы AmneziaVPN через doas pkill."""
        try:
            # Завершаем все процессы AmneziaVPN
            subprocess.run(['doas', 'pkill', '-f', 'AmneziaVPN'], check=False)
            logger.info("Процессы AmneziaVPN завершены через doas")
        except Exception as e:
            logger.debug(f"Ошибка при завершении процессов: {e}")

    def is_running(self) -> bool:
        """Проверяет, запущен ли процесс AmneziaVPN (GUI клиент)."""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'AmneziaVPN'],
                capture_output=True, text=True
            )
            if result.returncode != 0 or not result.stdout.strip():
                return False

            # Проверяем что запущен именно GUI клиент (не только сервис)
            # Сервис работает от root, клиент от пользователя
            processes = result.stdout.strip().split('\n')
            for pid in processes:
                try:
                    # Читаем cmdline процесса
                    with open(f'/proc/{pid}/cmdline', 'r') as f:
                        cmdline = f.read()
                        # Если это клиентский процесс (не сервис)
                        if 'client/bin/AmneziaVPN' in cmdline or '/usr/bin/AmneziaVPN' in cmdline:
                            return True
                except (FileNotFoundError, PermissionError):
                    continue
            return False
        except Exception:
            return False

    def is_connected(self) -> bool:
        """Проверяет, активен ли VPN по наличию интерфейса tun2."""
        try:
            result = subprocess.run(
                ['ip', 'link', 'show', self.interface_name],
                capture_output=True, text=True
            )
            # Проверяем что интерфейс существует и в состоянии UP
            return result.returncode == 0 and 'UP' in result.stdout
        except Exception:
            return False

    def connect(self) -> str:
        """
        Запускает VPN через CLI клиент.

        CLI создаёт GUI процесс который:
        1. Подключается к сервису AmneziaVPN-service
        2. Сервис запускает tun2socks
        3. Создаётся интерфейс tun2

        Если GUI уже запущен — проверяем подключение.
        """
        # 1. Если уже подключено и процесс есть — ничего не делаем
        if self.is_connected() and self.is_running():
            return "✅ VPN уже подключён"

        # 2. Если интерфейс есть, но процесса нет — завис, убиваем
        if self.is_connected() and not self.is_running():
            logger.info("VPN интерфейс есть, но процесс не найден. Очищаем...")
            self._kill_existing_processes()

        # 3. Если GUI запущен, но не подключён — ждём 5 сек
        if self.is_running() and not self.is_connected():
            logger.info("GUI запущен, но не подключается. Перезапускаем...")
            self._kill_existing_processes()

        try:
            # Запускаем CLI клиент в фоне
            proc = subprocess.Popen(
                [self.executable, '--connect', str(self.server_index)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True
            )
            logger.info(f"Запущен AmneziaVPN CLI (PID {proc.pid})")

            # Ждём появления интерфейса (до 10 секунд, проверка каждые 0.5 сек)
            for i in range(20):
                time.sleep(0.5)
                if self.is_connected():
                    return f"✅ VPN подключён (сервер {self.server_index})"

                # Проверяем, не упал ли процесс
                if proc.poll() is not None:
                    return f"❌ Процесс AmneziaVPN завершился с кодом {proc.returncode}"

            return "❌ Не удалось подключиться: интерфейс tun2 не появился за 10 сек"

        except FileNotFoundError:
            return f"❌ Исполняемый файл не найден: {self.executable}"
        except Exception as e:
            logger.exception("Ошибка при подключении VPN")
            return f"❌ Ошибка: {e}"

    def disconnect(self) -> str:
        """Завершает все процессы AmneziaVPN через doas pkill."""
        if not self.is_connected():
            return "✅ VPN уже отключён"

        try:
            # Завершаем все процессы AmneziaVPN
            subprocess.run(['doas', 'pkill', '-f', 'AmneziaVPN'], check=False)

            if not self.is_connected():
                return "✅ VPN отключён"

            return "❌ Не удалось отключить VPN: интерфейс tun2 всё ещё существует"

        except Exception as e:
            logger.exception("Ошибка при отключении VPN")
            return f"❌ Ошибка: {e}"
