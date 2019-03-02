/** [at]healeycodes
 * EmojiStreamer Factory
 * @param {ChildProcess} process anything that pipes emoji to stdout, one per line
 * @returns an express/express-ws app
 */
const app = (process) => {
    const { spawn } = require('child_process');
    const express = require('express');
    const app = express();
    require('express-ws')(app);

    app.use(express.static('public'));

    // Dashboard page avaliable at root or /dashboard.html
    app.get('/', (req, res) => {
        res.sendFile(path.join(__dirname + 'public/dashboard.html'));
    });

    // Collect WebSocket connections via /stream
    const clients = new Set();
    app.ws('/stream', (ws, req) => {
        clients.add(ws);
    });

    /* Whenever new emojis are ready, clear up CLOSING/CLOSED connections
       while sending emojis to the remaining clients */
    const emojiStreamer = process;
    emojiStreamer.stdout.on('data', (emoji) => {
        emoji = `${emoji}`;
        Array.from(clients, client => {
            if (client.readyState > 1) {
                clients.delete(client);
                return
            }
            client.send(emoji);
        });
    });
    emojiStreamer.stderr.on('data', (err) => {
        console.error(`${err}`);
    });
    emojiStreamer.on('close', (code) => {
        console.error(`Emoji source exited with code ${code}!`);
        process.exit(1);
    });

    return app;
}
module.exports = app;
