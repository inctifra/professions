import "./globals";
import "./libs/main.js";
import "./core.js";
import { stickyFn } from "./libs/main.js";
import "./site/index";


(() => {
  window.addEventListener('DOMContentLoaded', stickyFn);
})();
