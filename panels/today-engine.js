async function loadTodayPanel() {
  try {
    const response = await fetch("../data/today.json", { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Failed to load today.json: ${response.status}`);
    }

    const data = await response.json();
    renderList("workList", data.work);
    renderList("homeList", data.home);
    renderList("alertsList", data.alerts);
    document.getElementById("chaosScore").textContent = data.chaos ?? "N/A";
  } catch (error) {
    renderList("alertsList", ["Today panel data could not be loaded."]);
    document.getElementById("chaosScore").textContent = "N/A";
    console.error(error);
  }
}

function renderList(elementId, items = []) {
  const list = document.getElementById(elementId);
  list.innerHTML = "";

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });
}

loadTodayPanel();
