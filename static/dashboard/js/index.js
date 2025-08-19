import "../scss/main.scss";
import "./globals.js";
import "./libs/main.js";
import "./core.js";
import  { getCsrfToken, stickyFn } from "./libs/main.js";
import "./site/index";
import "./forms/plans/index.js";
import "./forms/projects/index.js";
import { Popover } from "bootstrap";


(() => {
  window.addEventListener('DOMContentLoaded', () => {
    stickyFn();

    if (document.getElementById("usageChart")) {
      import("./charts/dashboard").then(({ default: dashboardStat }) => {
        dashboardStat();
      })
    }
  });


  /**
   * @action key deletion
   * @params key_id
   */

document.addEventListener("click", function (e) {
  if (e.target.classList.contains("key-deletion")) {
    e.preventDefault();

    const $btn = $(e.target);
    const itemKeyId = $btn.data("key-id");
    const parentRow = $(`tr[data-key-id='${itemKeyId}']`);
    $.post($btn.data("endpoint"), { csrfmiddlewaretoken: getCsrfToken() })
      .done(async () => {
        const { InvalidateAndLoadNewKeys } = await import("./forms/projects/snippets.js");
        const popoverTrigger = document.querySelector(`[data-bs-toggle="popover"][data-key-id="${itemKeyId}"]`);
        const popoverInstance = Popover.getInstance(popoverTrigger);
        if (popoverInstance) {
          popoverInstance.dispose();
        }
        if (parentRow) {
          parentRow.remove();
        }
        InvalidateAndLoadNewKeys();
      })
      .fail((err) => {
        console.error("Delete failed", err);
      });
  }
});
})();


