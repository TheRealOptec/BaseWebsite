
export interface ISimplesErrorChannel {
    reportError(err: string): void;
    clearErrors(): void;
}
