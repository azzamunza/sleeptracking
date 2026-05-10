const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('C:\\\\Users\\\\Aaron Munro\\\\Documents\\\\GitHub\\\\sleeptracking\\\\index.html', 'utf8');
const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'https://azzamunza.github.io/sleeptracking/' });

setTimeout(() => {
    console.log('Errors:', dom.window._documentErrors || 'None');
}, 1000);
