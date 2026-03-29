import type { ISimplesErrorChannel } from "../ISimplesErrorChannel.js";

export class HTMLErrorChannel implements ISimplesErrorChannel {

    private htmlErrorElem: HTMLElement;

    public constructor(htmlErrorElem: HTMLElement) {
        this.htmlErrorElem = htmlErrorElem;
    }
    public clearErrors(): void {
        this.clearChannel();
    }

    private clearChannel(): void {
        this.htmlErrorElem.innerHTML = "";
    }

    private addErrorReport(err: string): void {
        this.htmlErrorElem.innerText = err;
    }

    public reportError(err: string): void {
        console.log(err);
        this.clearChannel();
        this.addErrorReport(err);
    }
    
}
