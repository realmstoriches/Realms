import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

scripts = [
    "generate_dual_brain_manifest.py",
    "generate_agent_variants.py",
    "generate_physical_descriptions.py",
    "fuse_agent_traits.py",
    "assign_crews_and_roles.py",
    "generate_team_roster.py"
]

def run_script(script_name):
    try:
        logging.info(f"🚀 Running {script_name}...")
        subprocess.run(["python", script_name], check=True)
        logging.info(f"✅ Completed {script_name}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error running {script_name}: {e}")

if __name__ == "__main__":
    for script in scripts:
        run_script(script)

    logging.info("🎉 All agent deployment scripts executed successfully.")