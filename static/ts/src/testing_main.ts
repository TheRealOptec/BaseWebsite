import { SimplesCompiler } from './posts/simples/SimplesCompiler.js';
import {} from './posts/simples/NodeInit.js'; // Initialise compiler nodes
import { ApiHandler } from './utils/apis/ApiHandler.js';

const frag = SimplesCompiler.compile(`
<simples>
    <h>My First Post!</h>
    <p>
        Here's some music I like:
        <embed>
            <news
                topic="Apple"
                from="2026-03-24"
                sortby="popularity&"
            />
        </embed>
    </p>
</simples>
`);
document.body.appendChild(frag);

ApiHandler.requestApi(json => console.log(json));