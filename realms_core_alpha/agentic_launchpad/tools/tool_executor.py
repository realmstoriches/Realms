import os
import subprocess

def execute_tool(file_path):
    ext = os.path.splitext(file_path)[1]

    if ext == ".js":
        print(f"🧪 Validating JavaScript: {file_path}")
        try:
            subprocess.run(["node", "--check", file_path], check=True)
        except Exception as e:
            print(f"❌ JS validation failed: {e}")
    elif ext == ".md":
        print(f"📄 Markdown output stored: {file_path}")
    elif ext == ".json":
        print(f"🔧 Config file saved: {file_path}")
    else:
        print(f"⚠️ Unknown file type: {file_path}")