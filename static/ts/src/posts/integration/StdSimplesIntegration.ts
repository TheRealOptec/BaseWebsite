import { SimplesIntegrator } from "./SimplesIntegrator.js";
import {} from '../simples/NodeInit.js'; // Initialise compiler nodes

// JS Hack
(function() {
    const editors = document.querySelectorAll(".simplesEditor");
    for(let editor of editors) {
        SimplesIntegrator.classPiped(<HTMLElement> editor, false);
    }
})();
