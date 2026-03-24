import { EmbedNode } from "../embedNode.js";
export class NewsNode {
    constructor() {
        EmbedNode.addEmbedNode("news", this);
    }
    static getInstance() {
        if (NewsNode.instance === null)
            return new NewsNode();
        return NewsNode.instance;
    }
    compile(fragHead, node) {
    }
}
NewsNode.instance = null;
//# sourceMappingURL=newsNode.js.map