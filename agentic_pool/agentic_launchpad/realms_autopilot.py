import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))


def run_all():
    queue_post()
    dispatch()

if __name__ == "__main__":
    run_all()