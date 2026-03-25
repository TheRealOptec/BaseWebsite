import { SimplesCompiler } from "../../../SimplesCompiler.js";
import { NewsNode } from "./newsNode.js";
export class NewsTopNode {
    constructor() {
        NewsNode.addCompilerNode("top", this);
    }
    static getInstance() {
        if (this.instance === null)
            NewsTopNode.instance = new NewsTopNode();
        return this.instance;
    }
    compile(fragHead, node, params) {
        if (node.textContent !== null) {
            const req = params["options"];
            if (req === undefined) {
                return;
            }
            req["top"] = node.textContent;
        }
        else
            SimplesCompiler.reportError("No content provided to from tag - content required");
    }
}
NewsTopNode.instance = null;
//# sourceMappingURL=newsTopNode.js.map