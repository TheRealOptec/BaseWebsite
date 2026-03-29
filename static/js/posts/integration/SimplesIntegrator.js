import { SimplesCompiler } from "../simples/SimplesCompiler.js";
export class SimplesIntegrator {
    static pipeSimplesCode(simples, pipedTo) {
        SimplesCompiler.compile(simples).then(frag => {
            // Clear content of pipe
            pipedTo.innerHTML = "";
            // Pipe compiled simples
            pipedTo.appendChild(frag);
        });
    }
    // Assumes editor is textarea or variation thereof which uses innerText as its content
    static pipeSimplesEditor(editor, pipedTo, useValue = false) {
        const simplesCode = useValue ? editor.value : editor.textContent;
        this.pipeSimplesCode(simplesCode, pipedTo);
    }
    static getClassParam(elem, prefix) {
        for (let cl of elem.className.split(" ")) {
            const clSplit = cl.split("-");
            if (clSplit.length != 2)
                continue;
            if (clSplit[0] == prefix) {
                return clSplit[1];
            }
        }
        return undefined;
    }
    static classPiped(editor, useValue = false) {
        const streamName = this.getClassParam(editor, this.SIMPLES_INPUT_CLASS_PREFIX);
        document.querySelectorAll(`.${this.SIMPLES_OUTPUT_CLASS_PREFIX}-${streamName}`).forEach(outputElem => {
            this.pipeSimplesEditor(editor, outputElem, useValue);
        });
    }
}
SimplesIntegrator.SIMPLES_OUTPUT_CLASS_PREFIX = "simplesout";
SimplesIntegrator.SIMPLES_INPUT_CLASS_PREFIX = "simplesin";
//# sourceMappingURL=SimplesIntegrator.js.map