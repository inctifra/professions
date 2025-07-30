import whiteLogo from "../../images/logo-white.svg";
import darkLogo from "../../images/logo-dark.svg";

export var rtl_flag = !1,
  dark_flag = !1;
export function layout_change_default() {
  const e = window.matchMedia("(prefers-color-scheme: dark)");
  let t = e.matches ? "dark" : "light";
  layout_change(t);
  const a = document.querySelector('.theme-layout .btn[data-value="default"]');
  a && a.classList.add("active"),
    e.addEventListener("change", (e) => {
      layout_change((t = e.matches ? "dark" : "light"));
    });
}
export function dark_mode() {
  var e = document.getElementById("dark-mode");
  e && layout_change(e.checked ? "dark" : "light");
}

export function layout_change(e) {
  const t = document.querySelector("body");
  document.querySelector(".pct-offcanvas");
  const a = document.querySelector('.theme-layout > a[data-value="default"]'),
    o = document.querySelector(".theme-layout > a.active");
  function c(e) {
    const t = whiteLogo,
      a = darkLogo;
    e = "dark" === e ? t : a;
    const o = document.querySelector(".pc-sidebar .m-header .logo-lg"),
      c = document.querySelector(".navbar-brand .logo-lg"),
      r = document.querySelector(".auth-main.v1 .auth-sidefooter img"),
      s = document.querySelector(".footer-top .footer-logo");
    o && o.setAttribute("src", e),
      c && c.setAttribute("src", e),
      r && r.setAttribute("src", e),
      s && s.setAttribute("src", e);
  }
  t.setAttribute("data-pc-theme", e),
    a && a.classList.remove("active"),
    "dark" === e
      ? ((dark_flag = !0),
        c("dark"),
        o &&
          (o.classList.remove("active"),
          document
            .querySelector(".theme-layout > a[data-value='true']")
            .classList.add("active")))
      : ((dark_flag = !1),
        c("light"),
        o &&
          (o.classList.remove("active"),
          document
            .querySelector(".theme-layout > a[data-value='false']")
            .classList.add("active")));
}
