// Load environment variables (requires dotenv-webpack plugin)
import axios from 'axios';

const chatbaseBotId = process.env.CHATBASE_PROJECT_ID;
const DOCS_API_URL = "/api/developers-docs/";
const TARGET_ELEMENT_ID = "docs-button-wrapper";

// Initialize Chatbase if not already initialized
if (!window.chatbase || window.chatbase("getState") !== "initialized") {
  window.chatbase = (...args) => {
    window.chatbase.q = window.chatbase.q || [];
    window.chatbase.q.push(args);
  };

  window.chatbase = new Proxy(window.chatbase, {
    get(target, prop) {
      if (prop === "q") return target.q;
      return (...args) => target(prop, ...args);
    },
  });
}

// Load Chatbase embed script
const onLoad = () => {
  const script = document.createElement("script");
  script.src = "https://www.chatbase.co/embed.min.js";
  script.id = chatbaseBotId;
  script.domain = "www.chatbase.co";
  document.body.appendChild(script);
};

// Insert floating docs button dynamically
const insertDocsButton = async () => {
  try {
    const response = await axios.get(DOCS_API_URL);
    const docsUrl = response?.data?.url;

    if (!docsUrl) return;

    const container = document.getElementById(TARGET_ELEMENT_ID);
    if (!container) {
      console.warn(`Element with ID "${TARGET_ELEMENT_ID}" not found.`);
      return;
    }

    const button = document.createElement("a");
    button.href = docsUrl;
    button.target = "_blank";
    button.title = "Check out our new documentation";
    button.className = "floating-docs-btn";
    button.innerText = "📘 New Docs Available";

    container.appendChild(button);
  } catch (error) {
    console.error("Failed to load documentation URL:", error);
  }
};

// Handle DOM loading
if (document.readyState === "complete") {
  onLoad();
  insertDocsButton();
} else {
  window.addEventListener("load", onLoad);
  window.addEventListener("DOMContentLoaded", insertDocsButton);
}

  document.addEventListener("contextmenu", (e) => {
    e.preventDefault();
  });

  document.addEventListener("keydown", (e) => {
    if (
      e.key === "F12" ||
      (e.ctrlKey && e.shiftKey && ["I", "J", "C"].includes(e.key)) ||
      (e.ctrlKey && e.key === "U")
    ) {
      e.preventDefault();
    }
  });

  document.addEventListener("selectstart", (e) => {
    e.preventDefault();
  });
  document.addEventListener("copy", (e) => {
    e.preventDefault();
    alert("Copying is disabled on this site.");
  });

  function isDesktop() {
    return !/Mobi|Android|iPad|iPhone/i.test(navigator.userAgent);
  }

  function detectDevTools() {
    const threshold = 160;
    const heightDiff = window.outerHeight - window.innerHeight;
    const widthDiff = window.outerWidth - window.innerWidth;
    return heightDiff > threshold || widthDiff > threshold;
  }

  function hardResetPage() {
    document.body.innerHTML = '';
    alert("Developer tools are not allowed!");
    window.location.reload(); // Optional
  }

  
  function showDevToolsWarning() {
    const modal = document.getElementById("devtools-warning-modal");
    document.body.classList.add("devtools-locked");
    if (modal) {
      modal.style.display = "block";
    }
  }

  if (isDesktop()) {
    setInterval(() => {
      if (detectDevTools()) {
        hardResetPage();
      }
    }, 1000);
  }


