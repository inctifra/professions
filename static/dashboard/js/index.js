import "./globals.js";
import "./libs/main.js";
import "./core.js";
import { stickyFn } from "./libs/main.js";
import "./site/index";
import "./forms/plans/index.js";


(() => {
  window.addEventListener('DOMContentLoaded', stickyFn);
})();
