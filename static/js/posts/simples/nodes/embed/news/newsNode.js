import { ApiHandler } from "../../../../../utils/apis/ApiHandler.js";
import { CompNodeParent } from "../../../CompNodeParent.js";
import { SimplesCompiler } from "../../../SimplesCompiler.js";
import { EmbedNode } from "../../embedNode.js";
export class NewsNode extends CompNodeParent {
    constructor() {
        super();
        EmbedNode.addCompilerNode("news", this);
    }
    static getInstance() {
        if (this.instance === null)
            this.instance = new NewsNode();
        return this.instance;
    }
    compileNewsNode(fragHead, node, params) {
        const newsNode = NewsNode.compNodes[node.nodeName];
        if (newsNode === undefined) {
            SimplesCompiler.reportError(`${node.nodeName} is not a valid news option`);
            return;
        }
        newsNode.compile(fragHead, node, params);
    }
    static addRequestResults(fragHead, options, json) {
        const articlesArr = json["articles"];
        if (options === undefined)
            return;
        const articlesCount = (options["top"] === undefined) ? articlesArr.length : options["top"];
        for (let i = 0; i < Math.min(articlesCount, articlesArr.length); i++) {
            const article = articlesArr[i];
            const elem = document.createElement("a");
            elem.innerHTML = article["title"];
            elem.setAttribute("href", article["url"]);
            fragHead.appendChild(elem);
        }
    }
    compile(fragHead, node, params) {
        const apiParams = {
            "req": { "api": "news" },
            "options": {}
        };
        for (let child of node.childNodes) {
            this.compileNewsNode(fragHead, child, apiParams);
        }
        ApiHandler.makeReq(json => {
            console.log(json);
            NewsNode.addRequestResults(fragHead, apiParams["options"], json);
        }, apiParams["req"]);
    }
}
NewsNode.instance = null;
//# sourceMappingURL=newsNode.js.map