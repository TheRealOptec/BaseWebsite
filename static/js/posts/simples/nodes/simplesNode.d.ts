import type { ISimplesNode } from "../ISimplesNode.js";
export declare class SimplesNode implements ISimplesNode {
    private static instance;
    private constructor();
    static getInstance(): ISimplesNode | null;
    compile(fragHead: Node, node: Node, params: Record<string, Record<string, string>>): void;
}
//# sourceMappingURL=simplesNode.d.ts.map