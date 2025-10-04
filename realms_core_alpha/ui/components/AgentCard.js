export function renderAgents(agents) {
  const container = document.getElementById("agents");
  container.innerHTML = "<h2>Agents</h2>";
  agents.forEach(agent => {
    const card = document.createElement("div");
    card.className = "agent-card";
    card.innerHTML = `<strong>${agent.name}</strong><br>${agent.role_title}<br><em>${agent.domain}</em>`;
    container.appendChild(card);
  });
}