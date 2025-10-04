import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config_manager import get_env

def run():
    print("Running PresidentAgent...")
    # Responsibilities:
    # - Oversee all agents
    # - Strategic decisions

if __name__ == "__main__":
    run()
