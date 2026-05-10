const fs = require('fs');
const html = fs.readFileSync('C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/index.html', 'utf-8');
const scriptMatch = html.match(/<script>(.*)<\/script>/s);

if (scriptMatch) {
    const jsCode = scriptMatch[1];
    fs.writeFileSync('C:/Users/Aaron Munro/Documents/GitHub/sleeptracking/test_syntax.js', jsCode);
    console.log("Extracted JS to test_syntax.js");
} else {
    console.log("No script tag found.");
}
