const EMOJI_STREAM = `ws://${window.location.host}/stream`;
const ws = new WebSocket(EMOJI_STREAM);

const status = document.querySelector('#status');
const con = document.querySelector('#emoji-con');

// Renders all emoji to our container
const render = (emoji) => {
    con.innerHTML += emoji;
}

ws.onopen = () => {
    status.innerHTML = 'Connected ✔️';
}

ws.onmessage = (emojis) => {
    // Multiple emoji may arrive delimited by a new-line char
    emojiList = emojis.data.split('\n');
    emojiList.splice(emojiList.length - 1);
    emojiList.forEach(emoji => {
        render(emoji);
    });
}

const explainer = document.querySelectorAll('.explainer');
explainer.forEach(exp => {
    exp.querySelectorAll('a').forEach(link => {
        link.onclick = () => {
            const text = exp.querySelector('p');
            text.classList.contains('hidden') ? text.classList.remove('hidden') : text.classList.add('hidden');
        }
    });
});