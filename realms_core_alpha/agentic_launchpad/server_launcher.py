import subprocess
import platform
import socket

def launch_servers():
    print("🔧 Launching backend services...")

    # Example: Launch local FastAPI server
    try:
        subprocess.Popen(["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"])
        print("✅ FastAPI server launched on port 8000")
    except Exception as e:
        print(f"❌ Failed to launch FastAPI: {e}")

    # Example: Check if port 8000 is open
    if is_port_open("localhost", 8000):
        print("🧠 Port 8000 is active.")
    else:
        print("⚠️ Port 8000 not responding.")

def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        return result == 0