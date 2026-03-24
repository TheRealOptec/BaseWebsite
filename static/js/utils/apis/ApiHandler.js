export class ApiHandler {
    static requestApi(apiFn) {
        fetch(this.API_ADDR)
            .then(response => response.json())
            .then(apiFn);
    }
}
ApiHandler.API_ADDR = "/mybase/apis";
//# sourceMappingURL=ApiHandler.js.map