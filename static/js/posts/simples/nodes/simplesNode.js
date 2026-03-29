import { SimplesCompiler } from "../SimplesCompiler.js";
// This node is just for backwards compability with old simple's posts
export class SimplesNode {
    constructor() {
        SimplesCompiler.addCompilerNode("simples", this);
    }
    static getInstance() {
        if (SimplesNode.instance === null)
            this.instance = new SimplesNode();
        return SimplesNode.instance;
    }
    compile(fragHead, node, params) {
        SimplesCompiler.compileNodeChildren(fragHead, node);
    }
}
SimplesNode.instance = null;
//# sourceMappingURL=simplesNode.js.map