import 'bootstrap';

import '@fortawesome/fontawesome-free/js/fontawesome'
import '@fortawesome/fontawesome-free/js/solid'
import '@fortawesome/fontawesome-free/js/regular'
import '@fortawesome/fontawesome-free/js/brands'

import "../sass/index.scss";


import "./nav-switch.ts";
import "./donate.ts"
import {initReloadScriptsOnContentRefresh} from "./reload";

initReloadScriptsOnContentRefresh();