import { SimplesIntegrator } from "./SimplesIntegrator.js";
import {} from '../simples/NodeInit.js'; // Initialise compiler nodes
import type { ISimplesErrorChannel } from "../simples/ISimplesErrorChannel.js";
import { SimplesCompiler } from "../simples/SimplesCompiler.js";

export function integrateSimples(useValue: boolean, errChannel: ISimplesErrorChannel|undefined = undefined) {
    if(errChannel !== undefined) SimplesCompiler.setStdError(errChannel);
    const editors = document.querySelectorAll(".simplesEditor");
    for(let editor of editors) {
        SimplesIntegrator.classPiped(<HTMLElement>editor, useValue);
    }
}
