import type { ISimplesNode } from "../ISimplesNode.js";
export declare class EmbedNode implements ISimplesNode {
    private static instance;
    private static embedNodes;
    private constructor();
    static getInstance(): ISimplesNode;
    static addEmbedNode(name: string, node: ISimplesNode): void;
    private compileEmbedNode;
    compile(fragHead: Node, node: ChildNode): void;
}
//# sourceMappingURL=embedNode.d.ts.map