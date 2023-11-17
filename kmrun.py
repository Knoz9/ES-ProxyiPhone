import subprocess
import os

cwd = os.getcwd()

script_path = f'{cwd}/kmscript.py'
updater_path = f'{cwd}/kmupdater.py'
restart_on_exit_code = 42  # Or any other specific number

# Flag to check if kmupdater has been run
has_run_updater = False

# If kmupdater hasn't been run yet, run it
if not has_run_updater:
    subprocess.run(['python3', updater_path])
    has_run_updater = True

while True:
    proc = subprocess.run(['python3', script_path])
    print("Heartbeat kmrun")
    
    if proc.returncode != restart_on_exit_code:
        break
