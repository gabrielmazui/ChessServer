const createServerBtn = document.getElementById("create-server");
const playAiBtn = document.getElementById("play-ai");

const overlay = document.getElementById("overlay");
const closeOverlayBtn = document.getElementById("close-overlay");
const confirmCreateBtn = document.getElementById("confirm-create");
const bestOfSelect = document.getElementById("best-of");

/* ====== FAKE DATA ====== */
const runningServers = [
  {
    id: "A9F2KQ",
    players: "mazui x mazui2",
    spectators: 4,
    bestOf: 5,
    round: "2/5"
  }
];

const waitingServers = [
  {
    id: "B7K2M9",
    player: "lucas",
    bestOf: 7
  }
];

/* ====== RENDER ====== */
function renderServers() {
  const running = document.getElementById("running-servers");
  const waiting = document.getElementById("waiting-servers");

  running.innerHTML = "";
  waiting.innerHTML = "";

  runningServers.forEach(s => {
    const card = document.createElement("div");
    card.className = "server-card";

    card.innerHTML = `
      <div class="server-info">
        <strong>${s.players}</strong>
        <span>BO${s.bestOf} • Round ${s.round}</span>
        <span>👀 ${s.spectators} spectators</span>
      </div>
      <div class="server-actions">
        <button type="button">Watch</button>
      </div>
    `;

    running.appendChild(card);
  });

  waitingServers.forEach(s => {
    const card = document.createElement("div");
    card.className = "server-card";

    card.innerHTML = `
      <div class="server-info">
        <strong>${s.player}</strong>
        <span>BO${s.bestOf} • Waiting for player...</span>
      </div>
      <div class="server-actions">
        <button type="button">Join</button>
      </div>
    `;

    card.querySelector("button").addEventListener("click", () => {
      window.location.href = `/room/${s.id}`;
    });

    waiting.appendChild(card);
  });
}

/* ====== EVENTS ====== */
createServerBtn.addEventListener("click", (e) => {
  console.log("ddd");
  e.preventDefault();
  overlay.style.display = "flex";
});

// fechar overlay create match
closeOverlayBtn.addEventListener("click", () => {
    overlay.style.display = "none";
});

overlay.addEventListener("click", (e) => {
  if (e.target === overlay) {
    overlay.style.display = "none";
  }
});

let selectedBO = 5;

document.querySelectorAll(".bo-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".bo-card").forEach(c =>
      c.classList.remove("selected")
    );
    card.classList.add("selected");
    selectedBO = card.dataset.bo;
  });
});

confirmCreateBtn.addEventListener("click", () => {
  console.log("Creating match - BO" + selectedBO);

  document.body.style.pointerEvents = "none";
  overlay.style.pointerEvents = "auto";
});

/* ====== INIT ====== */
renderServers();
