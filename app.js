/** [at]healeycodes
 * EmojiStreamer - app factory
 * @param {ChildProcess} process anything that pipes emoji to stdout, one per line
 * @returns an express/express-ws app
 */
const app = (process) => {
    const express = require('express');
    const app = express();
    require('express-ws')(app);

    app.use(express.static('public'));

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

    return app;
}
module.exports = app;
