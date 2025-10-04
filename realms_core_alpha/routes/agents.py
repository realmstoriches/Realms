from fastapi import APIRouter
router = APIRouter()
def load_manifest():
    print('📦 Manifest loaded')
    return {}
