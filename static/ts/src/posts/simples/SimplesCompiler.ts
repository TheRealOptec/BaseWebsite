import { ConsoleErrorChannel } from './error_handling/ConsoleErrorChannel.js';
import type { ISimplesErrorChannel } from './ISimplesErrorChannel.js';
import type { ISimplesNode } from './ISimplesNode.js';
import { SimplesParser } from './SimplesParser.js';

export class SimplesCompiler {

    private static compilerNodes: Record<string, ISimplesNode> = {};
    // The standard error handler for the simples complier
    private static stdErr: ISimplesErrorChannel = new ConsoleErrorChannel();

    // The number of unresolved promises created in execution
    private static promises: Promise<any>[] = [];

    public static addCompilerNode(name: string, compNode: ISimplesNode): void {
        this.compilerNodes[name] = compNode;
    }

    public static addPromise(promise: Promise<any>): void {
        this.promises.push(promise);
    }

    public static async compile(content: string): Promise<DocumentFragment> {
        return this.compilePure(`<simples> ${content} </simples>`);
    }

    public static async compilePure(content: string): Promise<DocumentFragment> {
        // Reset promises
        this.promises = [];
        // Clear error channel
        this.stdErr.clearErrors();

        const frag = SimplesCompiler.interpretXML(
            document.createDocumentFragment(),
            SimplesParser.parse(content)
        );
        await Promise.all(this.promises);
        return frag;
    }
    private static interpretXML(frag: DocumentFragment, xml: Document): DocumentFragment {
        return SimplesCompiler.interpretNodeList(frag, xml.documentElement.childNodes);
    }
    private static interpretNodeList(frag: DocumentFragment, nodes : NodeListOf<ChildNode>): DocumentFragment {
        for(let node of nodes) {
            frag = this.interpretNode(frag, node);
        }
        return frag;
    }

    public static getCompilerNode(name: string): ISimplesNode | undefined {
        return this.compilerNodes[name];
    }

    public static compileNodeChildren(fragHead: Node, node: Node): void {
        for(let child of node.childNodes) {
            const compNode = SimplesCompiler.getCompilerNode(child.nodeName);
            if(compNode === undefined) {
                this.stdErr.reportError(`${child.nodeName} is not a defined Simples element`);
                return;
            }
            compNode.compile(fragHead, child, {});
        }
    }

    private static interpretNode(frag: DocumentFragment, node: ChildNode): DocumentFragment {
        const compNode: ISimplesNode | undefined = this.compilerNodes[node.nodeName];
        if(compNode === undefined) {
            this.stdErr.reportError(`${node.nodeName} is not a defined Simples element`);
            return frag;
        }
        compNode.compile(frag, node, {});
        return frag;
    }

    public static reportError(msg: string): void {
        this.stdErr.reportError(msg);
    }

    public static setStdError(errorChannel: ISimplesErrorChannel): void {
        this.stdErr = errorChannel;
    }
}
