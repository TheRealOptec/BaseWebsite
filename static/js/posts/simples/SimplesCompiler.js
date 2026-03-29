var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { ConsoleErrorChannel } from './error_handling/ConsoleErrorChannel.js';
import { SimplesParser } from './SimplesParser.js';
export class SimplesCompiler {
    static addCompilerNode(name, compNode) {
        this.compilerNodes[name] = compNode;
    }
    static addPromise(promise) {
        this.promises.push(promise);
    }
    static compile(content) {
        return __awaiter(this, void 0, void 0, function* () {
            return this.compilePure(`<simples> ${content} </simples>`);
        });
    }
    static compilePure(content) {
        return __awaiter(this, void 0, void 0, function* () {
            // Reset promises
            this.promises = [];
            // Clear error channel
            this.stdErr.clearErrors();
            const frag = SimplesCompiler.interpretXML(document.createDocumentFragment(), SimplesParser.parse(content));
            yield Promise.all(this.promises);
            return frag;
        });
    }
    static interpretXML(frag, xml) {
        return SimplesCompiler.interpretNodeList(frag, xml.documentElement.childNodes);
    }
    static interpretNodeList(frag, nodes) {
        for (let node of nodes) {
            frag = this.interpretNode(frag, node);
        }
        return frag;
    }
    static getCompilerNode(name) {
        return this.compilerNodes[name];
    }
    static compileNodeChildren(fragHead, node) {
        for (let child of node.childNodes) {
            const compNode = SimplesCompiler.getCompilerNode(child.nodeName);
            if (compNode === undefined) {
                this.stdErr.reportError(`${child.nodeName} is not a defined Simples element`);
                return;
            }
            compNode.compile(fragHead, child, {});
        }
    }
    static interpretNode(frag, node) {
        const compNode = this.compilerNodes[node.nodeName];
        if (compNode === undefined) {
            this.stdErr.reportError(`${node.nodeName} is not a defined Simples element`);
            return frag;
        }
        compNode.compile(frag, node, {});
        return frag;
    }
    static reportError(msg) {
        this.stdErr.reportError(msg);
    }
    static setStdError(errorChannel) {
        this.stdErr = errorChannel;
    }
}
SimplesCompiler.compilerNodes = {};
// The standard error handler for the simples complier
SimplesCompiler.stdErr = new ConsoleErrorChannel();
// The number of unresolved promises created in execution
SimplesCompiler.promises = [];
//# sourceMappingURL=SimplesCompiler.js.map