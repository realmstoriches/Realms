from fastapi import APIRouter
import json

router = APIRouter()

@router.get("/")
def get_missions():
    with open("agentic_launchpad/mission_queue.json", "r") as f:
        return json.load(f)