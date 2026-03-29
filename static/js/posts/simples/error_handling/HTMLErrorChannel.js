export class HTMLErrorChannel {
    constructor(htmlErrorElem) {
        this.htmlErrorElem = htmlErrorElem;
    }
    clearErrors() {
        this.clearChannel();
    }
    clearChannel() {
        this.htmlErrorElem.innerHTML = "";
    }
    addErrorReport(err) {
        this.htmlErrorElem.innerText = err;
    }
    reportError(err) {
        console.log(err);
        this.clearChannel();
        this.addErrorReport(err);
    }
}
//# sourceMappingURL=HTMLErrorChannel.js.map