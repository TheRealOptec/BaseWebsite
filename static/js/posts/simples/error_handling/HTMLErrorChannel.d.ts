import type { ISimplesErrorChannel } from "../ISimplesErrorChannel.js";
export declare class HTMLErrorChannel implements ISimplesErrorChannel {
    private htmlErrorElem;
    constructor(htmlErrorElem: HTMLElement);
    clearErrors(): void;
    private clearChannel;
    private addErrorReport;
    reportError(err: string): void;
}
//# sourceMappingURL=HTMLErrorChannel.d.ts.map