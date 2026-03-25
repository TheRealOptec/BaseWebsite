import { CompNodeParent } from "../../../CompNodeParent.js";
import type { ISimplesNode } from "../../../ISimplesNode.js";
export declare class NewsNode extends CompNodeParent implements ISimplesNode {
    private static instance;
    private constructor();
    static getInstance(): ISimplesNode | null;
    private compileNewsNode;
    private static addRequestResults;
    compile(fragHead: Node, node: Node, params: Record<string, Record<string, string>>): void;
}
//# sourceMappingURL=newsNode.d.ts.map