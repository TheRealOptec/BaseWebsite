import type { ISimplesNode } from "../ISimplesNode.js";
import { SimplesCompiler } from "../SimplesCompiler.js";

// This node is just for backwards compability with old simple's posts
export class SimplesNode implements ISimplesNode {

    private static instance: SimplesNode|null = null;

    private constructor() {
        SimplesCompiler.addCompilerNode("simples", this);
    }

    public static getInstance(): ISimplesNode|null {
        if(SimplesNode.instance === null) this.instance = new SimplesNode();
        return SimplesNode.instance;
    }

    public compile(fragHead: Node, node: Node, params: Record<string, Record<string, string>>): void {
        SimplesCompiler.compileNodeChildren(fragHead, node);
    }
}
