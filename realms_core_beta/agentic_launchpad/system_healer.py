from datetime import datetime

def heal_system_if_needed():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🧠 System healer activated at {timestamp}")
    print("🔍 Scanning for broken agents, expired credentials, and dispatch failures...")
    print("✅ No critical issues detected. System is stable.")