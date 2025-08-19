import '@popperjs/core';
import 'bootstrap';
import PureCounter from "@srexi/purecounterjs";
import $ from "jquery";
import Swiper from 'swiper';
import AOS from 'aos';



import 'select2';

window.Swiper = Swiper;
window.$ = $;
window.jQuery = $;


window.AOS = AOS;
window.Select2 = $.fn.select2;
window.PureCounter = PureCounter;
window.pure = new PureCounter();

(function($){
    $("slot[name='logo']").remove();

    $(document).ready(function() {
        $('select').select2({
            placeholder: 'select profession',
            allowClear: true,
        });
    });



})(window.$)

import "./libs/api.js";
