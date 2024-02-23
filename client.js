const request = require('request');
const stream = require('stream');
const pipeline = require('stream').pipeline;

const options = {
 'method': 'POST',
 'url': 'YOUR_PROJECT_URL',
 'headers': { 
  'Content-Type': 'application/json',
  'X-Banana-API-Key': 'YOUR_API_KEY'
},
 body: JSON.stringify({ "prompt": "what is your favourite color: ", "fast": true })
};

const readable = request(options);
const writable = new stream.Writable();

let curChunk = "";

writable._write = function(chunk, encoding, next) {
  curChunk += chunk.toString();
  while (curChunk.includes("\n")) {
    const [first, ...rest] = curChunk.split("\n");
    // parse first as JSON
    const parsed = JSON.parse(first);
    // write to stdout without newline
    process.stdout.write(parsed.text);
    curChunk = rest.join("\n");
  }

  next();
};

pipeline( readable, writable, function(err) {
   if (err) {
     console.error('Pipeline failed.', err);
   } else {
     console.log('Pipeline succeeded.');
   }
 }
);
