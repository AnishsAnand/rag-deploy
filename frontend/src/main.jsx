import React from "react";
import ReactDOM from "react-dom/client";
import ChatPopup from "./components/ChatPopup";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ChatPopup />
  </React.StrictMode>
);

// Register service worker
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/service-worker.js").then(
      (reg) => console.log("SW registered:", reg.scope),
      (err) => console.error("SW registration failed:", err)
    );
  });
}
