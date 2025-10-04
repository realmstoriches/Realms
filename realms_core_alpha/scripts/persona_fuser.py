def fuse_personas(agent_a, agent_b):
    fused_name = f"{agent_a.split()[0]}-{agent_b.split()[0]} Fusion"
    fused_role = "Hybrid Specialist"
    print(f"🧬 Fused persona created: {fused_name} as {fused_role}")
    return {"name": fused_name, "role": fused_role}