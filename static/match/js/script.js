let board = Array(9).fill(null);
let currentPlayer = "X";

let yourRole = null;   // player | spectator
let yourSymbol = null;

let scoreP1 = 0;
let scoreP2 = 0;
let bestOf = 5;
let round = 1;

/* ELEMENTS */
const cells = document.querySelectorAll(".cell");
const scoreEl = document.getElementById("score");
const turnEl = document.getElementById("turn-player");
const roundEl = document.getElementById("round");
const bestOfEl = document.getElementById("bestof");

const loading = document.getElementById("loading");
const waiting = document.getElementById("waiting");
const watch = document.getElementById("watch");
const overlay = document.getElementById("overlay");
const overlayTitle = document.getElementById("overlay-title");
const app = document.getElementById("app");

const overlayBtn = document.getElementById("overlay-btn");
const watchBtn = document.getElementById("watch-btn");

const chat = document.querySelector(".chat-messages");

const msg = document.createElement("div");

/* ===== UI HELPERS ===== */

function hideAll() {
  loading.classList.add("hidden");
  waiting.classList.add("hidden");
  watch.classList.add("hidden");
  overlay.classList.add("hidden");
}

function showLoading() {
  hideAll();
  app.style.display = "none";
  loading.classList.remove("hidden");
}

function waitForPlayers() {
  hideAll();
  app.style.display = "none";
  waiting.classList.remove("hidden");
}

function askSpectate() {
  hideAll();
  app.style.display = "none";
  watch.classList.remove("hidden");
}

function startGame(starting = "X") {
  hideAll();
  app.style.display = "block";
  resetBoard();
  currentPlayer = starting;
  updateTurn();
  updateScore();
}

function finishGame(winner) {
  hideAll();
  overlayTitle.textContent = `${winner} won the match!`;
  overlay.classList.remove("hidden");
}

/* ===== GAME ===== */

function resetBoard() {
  board.fill(null);
  cells.forEach(c => {
    c.textContent = "";
    c.classList.remove("x", "o");
  });
}

function updateTurn() {
  turnEl.textContent = currentPlayer;
  turnEl.className = currentPlayer === "X" ? "x" : "o";
}

function updateScore() {
  scoreEl.textContent = `${scoreP1} x ${scoreP2}`;
  roundEl.textContent = round;
  bestOfEl.textContent = bestOf;
}

cells.forEach(cell => {
  cell.onclick = () => {
    if (yourRole !== "player") return;
    if (currentPlayer !== yourSymbol) return;

    const i = cell.dataset.index;
    if (board[i]) return;

    board[i] = currentPlayer;
    cell.textContent = currentPlayer;
    cell.classList.add(currentPlayer === "X" ? "x" : "o");

    currentPlayer = currentPlayer === "X" ? "O" : "X";
    updateTurn();
  };
});

function printMessage(nick, message, isLocal = false) {
    const chat = document.querySelector(".chat-messages");

    const msg = document.createElement("div");
    msg.style.marginBottom = "10px";
    msg.style.display = "block"; // garante nova linha

    const name = document.createElement("span");
    name.textContent = nick + ": ";
    name.style.fontWeight = "bold";
    name.style.color = isLocal ? "#22c55e" : "#22d3ee";

    const text = document.createElement("span");
    text.textContent = message;
    text.style.color = "#e5e7eb";

    msg.appendChild(name);
    msg.appendChild(text);
    chat.appendChild(msg);

    chat.scrollTop = chat.scrollHeight;
}


function setupChatInput(nick) {
  const input = document.querySelector(".chat input");

  input.addEventListener("keydown", e => {
    if (e.key !== "Enter") return;

    const message = input.value.trim();
    if (!message) return;

    // print local message
    printMessage(nick, message, true);

    // futuramente:
    // socket.send(JSON.stringify({ nick, message }));

    input.value = "";
  });
}


/* BUTTONS */
overlayBtn.onclick = () => location.href = "/";
watchBtn.onclick = () => startGame("X");

/* ===== INIT FLOW ===== */

showLoading();

setTimeout(() => {
  setTimeout(() => {
    yourRole = "player";      // or "spectator"
    yourSymbol = "X";
    user = "aaa"

    // if spectator:
    // askSpectate();
    setupChatInput(user)
    startGame()
    

  }, 1500);

}, 1200);
