const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html', 'utf-8');

const virtualConsole = new jsdom.VirtualConsole();
virtualConsole.on("jsdomError", e => console.error("JSDOM Error:", e));
virtualConsole.on("error", e => console.error("Error:", e));
virtualConsole.on("warn", e => console.warn("Warn:", e));

const dom = new JSDOM(html, { runScripts: "dangerously", virtualConsole });
