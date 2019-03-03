/** [at]healeycodes
 * EmojiStreamer - test our express/express-ws app
 */
const WebSocket = require('ws');
const { spawn } = require('child_process');
const emojiPiper = spawn('python', [`${__dirname}/../emoji-piper.py`])
const app = require('../appFactory')(emojiPiper);

describe('App starts', () => {
    it('launches without error ', (done) => {
        const PORT = process.env.TESTPORT || 8080;
        const server = app.listen(PORT, () => {
            server.close()
            done();
        });
    });
})

describe('Emoji-streaming WebSocket is functional', () => {
    const PORT = process.env.TESTPORT || 8080;
    
    const server = app.listen(PORT, () => {
        const ws = new WebSocket('ws://localhost:8080/stream');

        it('accepts connections', (done) => {
            ws.on('open', () => {
                done();
            });
        }).timeout(5000)

        it('streams emojis', (done) => {
            let msgCount = 0;
            ws.on('message', (data) => {
                if (++msgCount === 5) {
                    server.close()
                    done();
                }
            });
        }).timeout(120000)
    });
})
