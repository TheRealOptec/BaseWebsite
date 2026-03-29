import { SimplesIntegrator } from "./SimplesIntegrator.js";
import {} from '../simples/NodeInit.js'; // Initialise compiler nodes

export function integrateSimples(useValue: boolean) {
    const editors = document.querySelectorAll(".simplesEditor");
    for(let editor of editors) {
        SimplesIntegrator.classPiped(<HTMLElement>editor, useValue);
    }
}
