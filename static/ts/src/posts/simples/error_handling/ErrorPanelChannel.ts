import type { ISimplesErrorChannel } from "../ISimplesErrorChannel.js";

export class ErrorPanelChannel implements ISimplesErrorChannel {

    private mainPanel: HTMLElement;
    private holdingPanel: HTMLElement;

    public constructor(mainPanel: HTMLElement, holdingPanel: HTMLElement) {
        this.mainPanel = mainPanel;
        this.holdingPanel = holdingPanel;
    }
    public clearErrors(): void {
        this.clearChannel();
    }

    private clearChannel(): void {
        this.mainPanel.innerHTML = "";
        this.holdingPanel.classList.add("d-none");
    }

    private addErrorReport(err: string): void {
        this.mainPanel.innerText = err;
        this.holdingPanel.classList.remove("d-none");
    }

    public reportError(err: string): void {
        console.log(err);
        this.clearChannel();
        this.addErrorReport(err);
    }
    
}
