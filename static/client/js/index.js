import "../scss/main.scss";
import "animate.css";
import "@popperjs/core";
import "bootstrap";

import "../../dashboard/js/fonts/custom-font.js";
import "../../dashboard/js/fonts/custom-ant-icon.js";
import "../../dashboard/js/site/main.js";
import "../../dashboard/js/site/pcoded.js";
import "../../dashboard/js/globals.js";
import  'jquery.marquee';
import {WOW} from "wowjs";


let ost = 0;
document.addEventListener("scroll", function () {
    let cOst = document.documentElement.scrollTop;
    if (cOst == 0) {
        document.querySelector(".navbar").classList.add("top-nav-collapse");
    } else if (cOst > ost) {
        document.querySelector(".navbar").classList.add("top-nav-collapse");
        document.querySelector(".navbar").classList.remove("default");
    } else {
        document.querySelector(".navbar").classList.add("default");
        document.querySelector(".navbar").classList.remove("top-nav-collapse");
    }

    // if (cOst > 500) {
    //     document.querySelector(".pc-landing-custmizer").classList.add("active");
    // } else {
    //     document.querySelector(".pc-landing-custmizer").classList.remove("active");
    // }
    ost = cOst;
});
// End [ Menu hide/show on scroll ]
var wow = new WOW({
    animateClass: "animated",
});
wow.init();
// light dark image start
function initComparisons() {
    var x, i;
    x = document.getElementsByClassName("img-comp-overlay");
    for (i = 0; i < x.length; i++) {
        compareImages(x[i]);
    }
    function compareImages(img) {
        var slider,
            img,
            clicked = 0,
            w,
            h;
        w = img.offsetWidth;
        h = img.offsetHeight;
        img.style.width = w / 2 + "px";
        /*create slider:*/
        slider = document.createElement("DIV");
        slider.setAttribute("class", "img-comp-slider ti ti-separator-vertical bg-primary");
        /*insert slider*/
        img.parentElement.insertBefore(slider, img);
        /*position the slider in the middle:*/
        slider.style.top = h / 2 - slider.offsetHeight / 2 + "px";
        slider.style.left = w / 2 - slider.offsetWidth / 2 + "px";
        /*execute a function when the mouse button is pressed:*/
        slider.addEventListener("mousedown", slideReady);
        /*and another function when the mouse button is released:*/
        window.addEventListener("mouseup", slideFinish);
        /*or touched (for touch screens:*/
        slider.addEventListener("touchstart", slideReady);
        /*and released (for touch screens:*/
        window.addEventListener("touchend", slideFinish);
        function slideReady(e) {
            /*prevent any other actions that may occur when moving over the image:*/
            e.preventDefault();
            /*the slider is now clicked and ready to move:*/
            clicked = 1;
            /*execute a function when the slider is moved:*/
            window.addEventListener("mousemove", slideMove);
            window.addEventListener("touchmove", slideMove);
        }
        function slideFinish() {
            /*the slider is no longer clicked:*/
            clicked = 0;
        }
        function slideMove(e) {
            var pos;
            /*if the slider is no longer clicked, exit this function:*/
            if (clicked == 0) return false;
            /*get the cursor's x position:*/
            pos = getCursorPos(e);
            /*prevent the slider from being positioned outside the image:*/
            if (pos < 0) pos = 0;
            if (pos > w) pos = w;
            /*execute a function that will resize the overlay image according to the cursor:*/
            slide(pos);
        }
        function getCursorPos(e) {
            var a,
                x = 0;
            e = e.changedTouches ? e.changedTouches[0] : e;
            /*get the x positions of the image:*/
            a = img.getBoundingClientRect();
            /*calculate the cursor's x coordinate, relative to the image:*/
            x = e.pageX - a.left;
            /*consider any page scrolling:*/
            x = x - window.pageXOffset;
            return x;
        }
        function slide(x) {
            /*resize the image:*/
            img.style.width = x + "px";
            /*position the slider:*/
            slider.style.left = img.offsetWidth - slider.offsetWidth / 2 + "px";
        }
    }
}
initComparisons();
// light dark image end
// marquee start
$(".marquee").marquee({
    duration: 500000,
    pauseOnHover: true,
    startVisible: true,
    duplicated: true,
});
$(".marquee-1").marquee({
    duration: 500000,
    pauseOnHover: true,
    startVisible: true,
    duplicated: true,
    direction: "right",
});


  // Define default theme settings globally
  window.themeSettings = {
    bodyClass: 'landing-page',
    pcDirection: 'ltr',
    pcPreset: 'preset-6',
    pcTheme: 'light',
    fontFamily: "'Public Sans', sans-serif"
  };

  // Attach function to window so it's globally accessible
  window.applyTheme = function (overrides = {}) {
    const body = document.body;
    const settings = { ...window.themeSettings, ...overrides };

    // Update global settings too (so next calls use updated values)
    window.themeSettings = settings;

    // Apply theme changes
    body.className = settings.bodyClass;
    body.setAttribute('data-pc-direction', settings.pcDirection);
    body.setAttribute('data-pc-preset', settings.pcPreset);
    body.setAttribute('data-pc-theme', settings.pcTheme);
    body.style.fontFamily = settings.fontFamily;
  };

  // Apply theme once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    window.applyTheme();
  });