"""
This module defines the company structure, roles, and employee generation logic.
"""
import random

# A simplified, NVIDIA-inspired organizational chart
ORG_CHART = {
    "Software": [
        {
            "title": "AI Infrastructure Engineer",
            "department": "Software",
            "responsibilities": [
                "Design and build scalable AI infrastructure.",
                "Optimize deep learning frameworks.",
                "Develop tools for data scientists."
            ],
            "skills": ["Python", "Kubernetes", "Docker", "TensorFlow", "PyTorch"],
            "tools": ["Jenkins", "Git", "Jira"]
        },
        {
            "title": "Graphics Driver Engineer",
            "department": "Software",
            "responsibilities": [
                "Develop and optimize graphics drivers for new GPUs.",
                "Debug and fix driver-level issues.",
                "Collaborate with hardware teams."
            ],
            "skills": ["C++", "CUDA", "Vulkan", "OpenGL", "Driver Development"],
            "tools": ["Perforce", "Visual Studio", "GDB"]
        }
    ],
    "Hardware": [
        {
            "title": "ASIC Design Engineer",
            "department": "Hardware",
            "responsibilities": [
                "Design and verify complex ASIC components.",
                "Work with Verilog and SystemVerilog.",
                "Perform synthesis and timing analysis."
            ],
            "skills": ["Verilog", "SystemVerilog", "ASIC Design", "UVM"],
            "tools": ["VCS", "Verdi", "Design Compiler"]
        }
    ],
    "Research": [
        {
            "title": "Research Scientist",
            "department": "Research",
            "responsibilities": [
                "Conduct research in deep learning and computer vision.",
                "Publish papers in top-tier conferences.",
                "Develop novel algorithms and models."
            ],
            "skills": ["Python", "PyTorch", "TensorFlow", "Deep Learning", "Computer Vision"],
            "tools": ["Jupyter", "Git", "LaTeX"]
        }
    ]
}

FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "River"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia"]

def generate_employee_file(role_definition: dict):
    """
    Generates a complete employee file for an agent based on a role definition.

    Args:
        role_definition (dict): A dictionary describing the role from the ORG_CHART.

    Returns:
        dict: A dictionary representing the complete employee file.
    """
    employee_id = f"{random.randint(10000, 99999)}"
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

    return {
        "name": name,
        "role_title": role_definition["title"],
        "employee_id": employee_id,
        "hourly_rate": round(random.uniform(50.0, 150.0), 2),
        "physical_description": f"A VR avatar for {name}.",
        "skill_matrix": role_definition["skills"],
        "knowledge_sources": [role_definition["department"]],
        "tool_access": role_definition["tools"],
        "decision_logs": []
    }