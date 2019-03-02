/** [at]healeycodes
 * EmojiStreamer - we consume our express/express-ws here. See appFactory.js and emoji-streamer.py
 */
const { spawn } = require('child_process');
const app = require('./appFactory')(spawn('python', ['./emoji-piper.py']));

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`EmojiStreamer listening on port ${PORT}`);
});
