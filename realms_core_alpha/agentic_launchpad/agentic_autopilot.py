import subprocess
import sys
import os
from pathlib import Path

BASE = Path("F:/Realms/realms_core_alpha/agentic_launchpad")
AGENTS = BASE / "agents"
BUSINESS = BASE / "business"
MODULES = BASE / "modules"
LEGAL = BASE / "legal"
MARKETING = BASE / "marketing"
SRC = BASE / "src"
TESTS = BASE / "tests"

def run(script, *args):
    print(f"🔹 Running {script} {' '.join(args)} ...")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BASE)
    subprocess.run([sys.executable, str(script), *args], check=True, cwd=BASE, env=env)

def main():
    print("🚀 Agentic Autopilot Activated")

    # Phase 1: Scaffold
    run(BASE / "launch_master.py")

    # Phase 2: Business Plan + HRM
    run(AGENTS / "business_plan_agent.py")
    run(AGENTS / "hrm_agent.py")

    # Phase 3: Agent Activation
    with open(BUSINESS / "company_structure.json") as f:
        import json
        roles = json.load(f)
        for role in roles:
            run(AGENTS / role["script"])

    # Phase 4: Operational Buildout
    run(AGENTS / "cto_agent.py")                     # Dev + CI/CD
    run(AGENTS / "cfo_agent.py")                     # Finance + Monetization
    run(AGENTS / "cmo_agent.py")                     # Marketing Strategy
    run(AGENTS / "marketing_content_agent.py")       # Blog + Social + Email
    run(AGENTS / "sales_agent.py")                   # Funnel + Lead Capture
    run(AGENTS / "legal_counsel_agent.py")           # Legal Docs + IPO Prep
    run(AGENTS / "devops_agent.py")                  # Make.com Scenario Finalization
    run(AGENTS / "ui_ux_designer_agent.py")          # Blog Design
    run(AGENTS / "software_developer_agent.py")      # Product Code
    run(AGENTS / "software_architect_agent.py")      # Architecture
    run(AGENTS / "qa_agent.py")                      # Tests
    run(AGENTS / "technical_writer_agent.py")        # Docs
    run(AGENTS / "customer_support_agent.py")        # Support System

    print("✅ All agents executed. System is live and monetizing.")

    # Optional: IPO Trigger
    run(AGENTS / "president_agent.py", "--go_public")

if __name__ == "__main__":
    main()