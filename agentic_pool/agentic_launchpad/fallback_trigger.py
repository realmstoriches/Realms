import subprocess
from pathlib import Path
BASE = Path(__file__).resolve().parent
REPAIR_CHAIN = ['syndication_master.py', 'realms_autopilot.py']
def run_repair(script_name):
    print(f'\n🔧 Repairing: {script_name}')
    try:
        subprocess.run(['python', str(BASE / script_name)], check=True)
        print(f'✅ Recovered: {script_name}')
    except subprocess.CalledProcessError as e:
        print(f'❌ Repair failed: {script_name} → {e}')
def check_and_trigger():
    print('\n🛡️ [fallback_trigger] Activating fallback recovery agents...')
    for script in REPAIR_CHAIN:
        run_repair(script)
    print('✅ Fallback recovery complete.')
