export function renderRoles(roles) {
  const container = document.getElementById("roles");
  container.innerHTML = "<h2>Roles</h2>";
  roles.forEach(role => {
    const card = document.createElement("div");
    card.className = "role-card";
    card.innerHTML = `<strong>${role.role_title}</strong><br>Domain: ${role.domain}<br>Agent: ${role.agent_name}`;
    container.appendChild(card);
  });
}