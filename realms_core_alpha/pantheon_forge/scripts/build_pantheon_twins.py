import os
import json

def build_agents():
    with open("pantheon_manifest.txt", "r") as f:
        for line in f:
            role_id, alpha, beta, agent_name, crew, role, department = line.strip().split(",")
            path = f"F:/agentic_launchpad/agents/{role_id}"
            os.makedirs(path, exist_ok=True)

            meta = {
                "agent_name": agent_name,
                "role": role,
                "crew": crew,
                "department": department,
                "alpha": alpha,
                "beta": beta
            }

            for brain in ["alpha", "beta", "agent"]:
                with open(f"{path}/{brain}.py", "w") as f_out:
                    f_out.write(f"# {brain} brain for {role_id}\n")
                    f_out.write(json.dumps(meta, indent=2))

if __name__ == "__main__":
    build_agents()