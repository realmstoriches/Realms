export function renderMissions(missions) {
  const container = document.getElementById("missions");
  container.innerHTML = "<h2>Missions</h2>";
  missions.forEach(mission => {
    const card = document.createElement("div");
    card.className = "mission-card";
    card.innerHTML = `<strong>${mission.mission_id}</strong><br>${mission.objective}<br>Assigned Crew: ${mission.assigned_crew}`;
    container.appendChild(card);
  });
}