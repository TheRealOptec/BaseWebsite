import type { ISimplesErrorChannel } from './ISimplesErrorChannel.js';
import type { ISimplesNode } from './ISimplesNode.js';
export declare class SimplesCompiler {
    private static compilerNodes;
    private static stdErr;
    private static promises;
    static addCompilerNode(name: string, compNode: ISimplesNode): void;
    static addPromise(promise: Promise<any>): void;
    static compile(content: string): Promise<DocumentFragment>;
    static compilePure(content: string): Promise<DocumentFragment>;
    private static interpretXML;
    private static interpretNodeList;
    static getCompilerNode(name: string): ISimplesNode | undefined;
    static compileNodeChildren(fragHead: Node, node: Node): void;
    private static interpretNode;
    static reportError(msg: string): void;
    static setStdError(errorChannel: ISimplesErrorChannel): void;
}
//# sourceMappingURL=SimplesCompiler.d.ts.map