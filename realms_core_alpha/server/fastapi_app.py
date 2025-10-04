# fastapi_app.py
# TODO: Build FastAPI endpoints
from fastapi import FastAPI
from routes import agents, crews, roles, tools, missions

app = FastAPI(title="Realms API")

app.include_router(agents.router, prefix="/api/agents")
app.include_router(crews.router, prefix="/api/crews")
app.include_router(roles.router, prefix="/api/roles")
app.include_router(tools.router, prefix="/api/tools")
app.include_router(missions.router, prefix="/api/missions")
