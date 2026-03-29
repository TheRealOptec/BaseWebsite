import type { ISimplesErrorChannel } from "../ISimplesErrorChannel.js";

export class ConsoleErrorChannel implements ISimplesErrorChannel {
    clearErrors(): void {
        // Do nothing - cannot clear errors
    }
    reportError(err: string): void {
        console.error(err);
    }
    
}
