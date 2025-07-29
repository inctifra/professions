import "./vendors.js";
import "./libs/main.js";
import "./core.js";
import { stickyFn } from "./libs/main.js";

(() => {
  window.addEventListener('scroll', stickyFn);
  window.addEventListener('DOMContentLoaded', stickyFn);
})();