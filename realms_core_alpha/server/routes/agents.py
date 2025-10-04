from fastapi import APIRouter
from manifest_loader import load_manifest

router = APIRouter()

@router.get("/")
def get_agents():
    manifest = load_manifest()
    return manifest["agents"]