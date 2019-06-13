const EMOJI_STREAM = `wss://${window.location.host}/stream`;
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
    let emojiList = emojis.data.split('\n');
    emojiList.splice(emojiList.length - 1);
    emojiList.forEach(emoji => {
        render(emoji);
    });
}

// Set up explainer toggle
let explainer = false;
const toggleable = document.querySelector('.toggleable'); // Cache everything because we like to go fast
const toggler = document.querySelector('.toggler');
const togglerText = toggler.innerText.slice(0, toggler.innerText.length-1);
document.querySelector('.explainer').onclick = () => {
    explainer = !explainer;
    toggler.innerText = togglerText + explainer === true ? '-' : '+';
    if (explainer === true) {
        toggleable.classList.remove('hidden');
        toggler.innerText = togglerText + '-';
    } else {
        toggleable.classList.add('hidden');
        toggler.innerText = togglerText + '+';
    }
  }
