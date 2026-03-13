from subprocess import run, check_output, CalledProcessError
from time import sleep

def shell(command: str):
    if ' ' in command:
        run(command.split(' '))
    run(command)

def get_pid_via_pgrep(process_name):
    try:
        output = check_output(['pgrep', process_name], text=True).strip()
        if '\n' in output:
            pids = [int(pid) for pid in output.split('\n') if pid]
            return pids
        else:
            if output:
                return output
            return []
    except CalledProcessError:
        return []  # процесс не найден

# app_pid = get_pid_via_pgrep('jarvis-app')
# gui_pid = get_pid_via_pgrep('jarvis-gui')


# FIX: после завершения джарвиса скрипт останавливается (заменить killall на kill $PID)
shell('killall jarvis-app')
shell('killall jarvis-gui')
sleep(1.5)
shell('/home/kasiro/Документы/jarvis/post_build.sh')
shell('/home/kasiro/Документы/jarvis/jarvis.sh')
