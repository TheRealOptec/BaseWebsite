import { SimplesCompiler } from "../SimplesCompiler.js";
export class EmbedNode {
    constructor() {
        SimplesCompiler.addCompilerNode("embed", this);
    }
    static getInstance() {
        if (EmbedNode.instance === null)
            return new EmbedNode();
        return EmbedNode.instance;
    }
    static addEmbedNode(name, node) {
        this.embedNodes[name] = node;
    }
    compileEmbedNode(node) {
        const embedNode = EmbedNode.embedNodes[node.nodeName];
    }
    compile(fragHead, node) {
        for (let child of node.childNodes) {
            this.compileEmbedNode(child);
        }
    }
}
EmbedNode.instance = null;
EmbedNode.embedNodes = {};
//# sourceMappingURL=embedNode.js.map