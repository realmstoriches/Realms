import json, logging
from assemble_crew import assemble_crew_for_mission
from task_router import route_task

logging.basicConfig(level=logging.INFO)

with open("agentic_launchpad/mission_queue.json") as f:
    missions = json.load(f)

with open("agentic_launchpad/company_manifest.json") as f:
    manifest = json.load(f)

for mission in missions:
    logging.info(f"🚀 Triggering mission {mission['mission_id']}")
    crew = assemble_crew_for_mission(mission, manifest)
    route_task(mission, crew, manifest)