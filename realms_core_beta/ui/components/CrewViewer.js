export function renderCrews(crews) {
  const container = document.getElementById("crews");
  container.innerHTML = "<h2>Crews</h2>";
  crews.forEach(crew => {
    const card = document.createElement("div");
    card.className = "crew-card";
    card.innerHTML = `<strong>${crew.crew}</strong><br>Members: ${crew.members.join(", ")}`;
    container.appendChild(card);
  });
}