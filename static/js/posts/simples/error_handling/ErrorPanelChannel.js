export class ErrorPanelChannel {
    constructor(mainPanel, holdingPanel) {
        this.mainPanel = mainPanel;
        this.holdingPanel = holdingPanel;
    }
    clearErrors() {
        this.clearChannel();
    }
    clearChannel() {
        this.mainPanel.innerHTML = "";
        this.holdingPanel.classList.add("d-none");
    }
    addErrorReport(err) {
        this.mainPanel.innerText = err;
        this.holdingPanel.classList.remove("d-none");
    }
    reportError(err) {
        console.log(err);
        this.clearChannel();
        this.addErrorReport(err);
    }
}
//# sourceMappingURL=ErrorPanelChannel.js.map