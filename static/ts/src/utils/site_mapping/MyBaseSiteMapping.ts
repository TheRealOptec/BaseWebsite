
/**
 * @description
 * This class is specifically defined for handling all site mapping related to the django mybase app
 */
class MyBaseSiteMapping {
    // The name of the my base django app
    public static readonly MYBASE: string = "mybase";
    // The url for the mybase django app
    public static readonly MYBASE_URL: string = `${window.location.hostname}/${MyBaseSiteMapping.MYBASE}/`;
    /**
     * @description
     * Redirects the user to the specified url.
     * @param url
     * The url to redirect the user to - will be relative to the mybase app base url
     */
    public static redirect(url: string): void {
        window.location.href = `${MyBaseSiteMapping.MYBASE_URL}${url}`;
    }
}
