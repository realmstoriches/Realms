import os

def generate_output(agent_name, role, mission, tools):
    output_dir = "generated_output"
    os.makedirs(output_dir, exist_ok=True)

    if "React" in tools or "UI" in role:
        ext = ".js"
    elif "Mermaid" in tools:
        ext = ".md"
    elif "Notion" in tools or "Google Docs" in tools:
        ext = ".md"
    elif "config" in role.lower():
        ext = ".json"
    else:
        ext = ".md"

    filename = f"{output_dir}/{agent_name.replace(' ', '_')}_{role.replace(' ', '_')}{ext}"

    with open(filename, "w", encoding="utf-8") as f:
        if ext == ".md":
            f.write(f"# Agent: {agent_name}\n**Role:** {role}\n**Mission:** {mission['objective']}\n**Tools:** {', '.join(tools)}\n\n")
        elif ext == ".json":
            f.write("{\n")
            f.write(f'  "agent": "{agent_name}",\n  "role": "{role}",\n  "mission": "{mission["objective"]}",\n  "tools": {tools}\n}}\n')
        elif ext == ".js":
            f.write(f"// Agent: {agent_name}\n// Role: {role}\n// Mission: {mission['objective']}\n// Tools: {', '.join(tools)}\n\n")
            f.write("export default function CrewCard() {\n  return <div>Crew Info</div>;\n}\n")

        if ext == ".md" and "Mermaid" in tools:
            f.write("```mermaid\nflowchart TD\n  A --> B\n```\n")

    return filename