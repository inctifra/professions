import '@popperjs/core';
import 'bootstrap';
import $ from "jquery";
import SimpleBar from 'simplebar';
import flatpickr from "flatpickr";
import axios from "axios";
import feather from 'feather-icons';
window.$ = $;
window.jQuery = $;
window.flatpickr = flatpickr;
window.SimpleBar = SimpleBar;
window.feather = feather;
import "slick-carousel";

import 'datatables.net-dt';
import 'datatables.net-buttons-dt';

// Export dependencies
import 'jszip';
import 'datatables.net-buttons/js/buttons.html5';
import 'datatables.net-buttons/js/buttons.print';

import { create, registerPlugin } from 'filepond';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';

registerPlugin(FilePondPluginImagePreview);


export {  $ as jQuery, $, flatpickr, FilePondPluginImagePreview, create, 
    registerPlugin, SimpleBar, axios, feather };
