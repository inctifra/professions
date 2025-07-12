import '@popperjs/core';
import 'bootstrap';
import PureCounter from "@srexi/purecounterjs";
import $ from "jquery";
import Swiper from 'swiper';
import AOS from 'aos';

window.Swiper = Swiper;
window.$ = $;
window.jQuery = $;


window.AOS = AOS;



window.PureCounter = PureCounter;
window.pure = new PureCounter();

(function($){
    $("slot[name='logo']").remove();
})(window.$)

import "./libs/api.js";
