import type { ISimplesErrorChannel } from "../ISimplesErrorChannel.js";
export declare class ErrorPanelChannel implements ISimplesErrorChannel {
    private mainPanel;
    private holdingPanel;
    constructor(mainPanel: HTMLElement, holdingPanel: HTMLElement);
    clearErrors(): void;
    private clearChannel;
    private addErrorReport;
    reportError(err: string): void;
}
//# sourceMappingURL=ErrorPanelChannel.d.ts.map