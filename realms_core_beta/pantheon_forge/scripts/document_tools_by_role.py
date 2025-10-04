import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

input_file = "real_minds.json"
output_file = "tools_manifest.json"

# ✅ Domain-to-tools map
tool_map = {
    "Project Management": ["Asana", "Jira", "GanttPro", "Trello"],
    "HR & Culture": ["BambooHR", "Workday", "15Five", "CultureAmp"],
    "Organizational Design": ["OrgVue", "Lucidchart", "Miro"],
    "Leadership & Strategy": ["OKRs", "Balanced Scorecard", "Cascade"],
    "DevOps": ["Docker", "Kubernetes", "Terraform", "GitHub Actions"],
    "Innovation": ["Notion", "Figma", "Mural"],
    "Finance": ["QuickBooks", "Xero", "Stripe", "Plaid"],
    "Marketing": ["HubSpot", "Mailchimp", "Canva", "Google Analytics"],
    "Design": ["Figma", "Sketch", "Adobe XD"],
    "Engineering": ["Git", "VS Code", "Postman", "Swagger"]
}

# ✅ Build manifest
with open(input_file, "r", encoding="utf-8") as f:
    minds = json.load(f)

manifest = {}
for mind in minds:
    domain = mind.get("domain", "")
    tools = tool_map.get(domain, ["Notion", "Google Docs"])
    manifest[mind["name"]] = {
        "domain": domain,
        "tools": tools,
        "preferred_stack": "Agile" if "Project" in domain or "DevOps" in domain else "OKRs"
    }

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=4)

logging.info(f"✅ tools_manifest.json written with {len(manifest)} entries")