const launcher = document.getElementById("chat-launcher");
const chatBox = document.getElementById("chat-box");
const messages = document.getElementById("chat-messages");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Toggle chat visibility
launcher.addEventListener("click", () => {
  const isVisible = chatBox.style.display === "flex";
  chatBox.style.display = isVisible ? "none" : "flex";
  if (!isVisible) input.focus();
});

function appendMessage(text, sender = "ai") {
  const msg = document.createElement("div");
  msg.className = "msg " + sender;
  msg.textContent = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  appendMessage(text, "user");
  input.value = "";
  appendMessage("🤖 ...", "ai"); // loading placeholder

  try {
    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    const data = await res.json();
    messages.lastChild.remove(); // remove loader
    appendMessage(data.answer || "No response 🤔", "ai");
  } catch (err) {
    messages.lastChild.remove();
    appendMessage("Oops, something went wrong! 😢", "ai");
  }
}

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendMessage();
});

// initial greeting
appendMessage(
  "Hi there! 👋 I'm your AI assistant. How can I help today?",
  "ai"
);
