import time

LOG = r"F:\Realms\logs\dispatch_log.txt"

def stream():
    print("📡 Live Dispatch Feed\n")
    with open(LOG, "r") as f:
        f.seek(0, 2)
        while True:
            if line := f.readline():
                print(line.strip())
            else:
                time.sleep(1)

if __name__ == "__main__":
    stream()