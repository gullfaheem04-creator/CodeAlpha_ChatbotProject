(function () {
  const launcher = document.getElementById("chat-launcher");
  const panel = document.getElementById("chat-panel");
  const closeBtn = document.getElementById("chat-close");
  const log = document.getElementById("chat-log");
  const chips = document.getElementById("chat-chips");
  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("chat-send");
  const navChat = document.getElementById("nav-chat");
  let greeted = false;

  function openChat() {
    panel.hidden = false;
    launcher.setAttribute("aria-expanded", "true");
    if (!greeted) {
      greeted = true;
      addMessage("Hi! I'm Brewie. Ask me about plans, delivery, orders or brewing.", "bot");
      setChips(["See plans", "Delivery time", "Track my order"]);
    }
    input.focus();
  }

  function closeChat() {
    panel.hidden = true;
    launcher.setAttribute("aria-expanded", "false");
    launcher.focus();
  }

  function addMessage(text, who) {
    const el = document.createElement("div");
    el.className = "msg " + who;
    el.textContent = text; // textContent prevents HTML injection
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  function setChips(items) {
    chips.replaceChildren();
    (items || []).forEach(function (label) {
      const b = document.createElement("button");
      b.className = "chip";
      b.type = "button";
      b.textContent = label;
      b.addEventListener("click", function () { send(label); });
      chips.appendChild(b);
    });
  }

  function showTyping() {
    const el = document.createElement("div");
    el.className = "msg bot typing";
    el.innerHTML = "<i></i><i></i><i></i>";
    el.setAttribute("aria-label", "Brewie is typing");
    log.appendChild(el);
    log.scrollTop = log.scrollHeight;
    return el;
  }

  async function send(text) {
    text = (text || "").trim();
    if (!text) return;
    addMessage(text, "user");
    input.value = "";
    setChips([]);
    sendBtn.disabled = true;
    const typing = showTyping();
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      typing.remove();
      if (!res.ok) {
        addMessage(data.error || "Something went wrong. Please try again.", "error");
      } else {
        addMessage(data.response, "bot");
        setChips(data.suggestions);
      }
    } catch (e) {
      typing.remove();
      addMessage("I can't reach the server. Check your connection and try again.", "error");
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  }

  launcher.addEventListener("click", openChat);
  navChat.addEventListener("click", function (e) { e.preventDefault(); openChat(); });
  closeBtn.addEventListener("click", closeChat);
  sendBtn.addEventListener("click", function () { send(input.value); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") { e.preventDefault(); send(input.value); }
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !panel.hidden) closeChat();
  });
})();
