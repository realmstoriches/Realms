import { renderAgents } from './components/AgentCard.js';
import { renderCrews } from './components/CrewViewer.js';
import { renderRoles } from './components/RoleMatrix.js';
import { renderMissions } from './components/MissionConsole.js';

fetch("/api/agents").then(res => res.json()).then(renderAgents);
fetch("/api/crews").then(res => res.json()).then(renderCrews);
fetch("/api/roles").then(res => res.json()).then(renderRoles);
fetch("/api/missions").then(res => res.json()).then(renderMissions);