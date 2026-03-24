
export class ApiHandler {
    private static API_ADDR: string = "/mybase/apis";

    public static requestApi(apiFn: ((value: any) => any)) {
        fetch(this.API_ADDR)
            .then(response => response.json())
            .then(apiFn);
    }
}
