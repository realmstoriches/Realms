from fastapi import FastAPI
from routes import agents, crews, roles, tools, missions

app = FastAPI(title="Realms API")

app.include_router(agents.router)
app.include_router(crews.router)
app.include_router(roles.router)
app.include_router(tools.router)
app.include_router(missions.router)