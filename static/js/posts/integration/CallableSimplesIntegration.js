import { SimplesIntegrator } from "./SimplesIntegrator.js";
import {} from '../simples/NodeInit.js'; // Initialise compiler nodes
import { SimplesCompiler } from "../simples/SimplesCompiler.js";
export function integrateSimples(useValue, errChannel = undefined) {
    if (errChannel !== undefined)
        SimplesCompiler.setStdError(errChannel);
    const editors = document.querySelectorAll(".simplesEditor");
    for (let editor of editors) {
        SimplesIntegrator.classPiped(editor, useValue);
    }
}
//# sourceMappingURL=CallableSimplesIntegration.js.map