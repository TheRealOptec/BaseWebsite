import { SimplesCompiler } from "../simples/SimplesCompiler.js";

export class SimplesIntegrator {

    private static SIMPLES_OUTPUT_CLASS_PREFIX: string = "simplesout";
    private static SIMPLES_INPUT_CLASS_PREFIX: string = "simplesin";

    public static pipeSimplesCode(simples: string, pipedTo: HTMLElement): void {
        SimplesCompiler.compile(simples).then(frag => {
            // Clear content of pipe
            pipedTo.innerHTML = "";
            // Pipe compiled simples
            pipedTo.appendChild(frag);
        });
    }
    // Assumes editor is textarea or variation thereof which uses innerText as its content
    public static pipeSimplesEditor(editor: HTMLElement, pipedTo: HTMLElement, useValue: boolean = false): void {
        const simplesCode: string = useValue ? (<HTMLInputElement>editor).value : editor.textContent;
        this.pipeSimplesCode(simplesCode, pipedTo);
    }
    private static getClassParam(elem: Element, prefix: string): string|undefined {
        for(let cl of elem.className.split(" ")) {
            const clSplit = cl.split("-");
            if(clSplit.length != 2) continue;
            if(clSplit[0] == prefix) {
                return clSplit[1];
            }
        }
        return undefined;
    }
    public static classPiped(editor: HTMLElement, useValue: boolean = false): void {
        const streamName = this.getClassParam(editor, this.SIMPLES_INPUT_CLASS_PREFIX);
        document.querySelectorAll(`.${this.SIMPLES_OUTPUT_CLASS_PREFIX}-${streamName}`).forEach(outputElem => {
            this.pipeSimplesEditor(editor, <HTMLElement>outputElem, useValue);
        });
    }
}
