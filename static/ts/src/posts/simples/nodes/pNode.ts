import type { ISimplesNode } from "../ISimplesNode.js";
import { SimplesCompiler } from "../SimplesCompiler.js";

export class PNode implements ISimplesNode {

    private static instance: PNode|null = null;

    private constructor() {
        SimplesCompiler.addCompilerNode("p", this);
    }

    public static getInstance(): ISimplesNode {
        if(PNode.instance === null) return new PNode();
        return PNode.instance;
    }

    public compile(fragHead: Node, node: ChildNode): void {
        const pElem = document.createElement("p");
        const test = new DocumentFragment();
        test.getRootNode().childNodes;
    }
}
