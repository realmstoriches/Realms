import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config_manager import get_env

def run():
    print("Running LegalCounselAgent...")
    # Responsibilities:
    # - Legal docs
    # - IPO prep

if __name__ == "__main__":
    run()
