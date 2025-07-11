import '@popperjs/core';
import 'bootstrap';
import $ from "jquery";

window.$ = $;
window.jQuery = $;

(function($){
    $("slot[name='logo']").remove();
})(window.$)