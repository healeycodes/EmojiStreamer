/** [at]healeycodes
 * EmojiStreamer - we consume our express/express-ws app here. See appFactory.js and emoji-streamer.py
 */
const { spawn } = require('child_process');
const emojiPiper = spawn('python', ['./emoji-piper.py'])
const app = require('./appFactory')(emojiPiper);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`EmojiStreamer listening on port ${PORT}`);
});
