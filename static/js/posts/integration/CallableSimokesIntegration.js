import { SimplesIntegrator } from "./SimplesIntegrator.js";
import {} from '../simples/NodeInit.js'; // Initialise compiler nodes
export function integrateSimples() {
    const editors = document.querySelectorAll(".simplesEditor");
    for (let editor of editors) {
        SimplesIntegrator.classPiped(editor);
    }
}
//# sourceMappingURL=CallableSimokesIntegration.js.map