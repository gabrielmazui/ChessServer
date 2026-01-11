// Overlay criar partida
const createServerBtn = document.getElementById("create-server");
const overlay = document.getElementById("overlay");
const closeOverlayBtn = document.getElementById("close-overlay");
const confirmCreateBtn = document.getElementById("confirm-create");

createServerBtn.addEventListener("click", () => overlay.style.display="flex");
closeOverlayBtn.addEventListener("click", () => overlay.style.display="none");
overlay.addEventListener("click", e => { if(e.target===overlay) overlay.style.display="none"; });

confirmCreateBtn.addEventListener("click", () => {
    console.log("Match created!");
    overlay.style.display="none";
    // Chame sua API para criar a partida aqui
});

const logo = document.getElementById("logo")
logo.addEventListener("click", () =>{
  window.location.href = "/";
})

const userArea = document.getElementById("user-area");
const logoutBtn = document.getElementById("logout-btn");

// abre / fecha ao clicar no username
userArea.addEventListener("click", (e) => {
  e.stopPropagation(); // impede fechar imediatamente
  logoutBtn.classList.toggle("show");
});

// click fora fecha
document.addEventListener("click", () => {
  logoutBtn.classList.remove("show");
});

// click no sair
logoutBtn.addEventListener("click", (e) => {
  e.stopPropagation(); // não fecha antes de executar
  console.log("Logout clicked");

  logoutBtn.classList.remove("show");
});


// Função para ouvir clicks nos matches
document.querySelectorAll(".join-btn").forEach(btn => {
  btn.addEventListener("click", () => {
      const matchId = btn.dataset.id;
      console.log("Joining match", matchId);
      window.location.href = `/room/${matchId}`;
  });
});

document.querySelectorAll(".watch-btn").forEach(btn => {
  btn.addEventListener("click", () => {
      const matchId = btn.dataset.id;
      console.log("Watching match", matchId);
      window.location.href = `/room/${matchId}`;
  });
});
