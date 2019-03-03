[![Build Status](https://travis-ci.org/healeycodes/EmojiStreamer.svg?branch=master)](https://travis-ci.org/healeycodes/EmojiStreamer)

## EmojiStreamer

Real-time streaming of any emojis within comments posted to Reddit!


![EmojiStreamer](https://github.com/healeycodes/EmojiStreamer/blob/master/preview.gif)

<br>

### How does it work?

Every comment posted to Reddit is scanned for emojis using PRAW (The Python Reddit API Wrapper). 

The 'scanner' is a Python child process of a Node.js app. Should an emoji be found, it's piped to the Node.js app. 

From there, emojis are sent to every connected WebSocket client (a.k.a. you!) 👍

<br>

### Travis CI / Testing

Test builds are ran for every commit to master at the moment.

This project uses integration testing to ensure that the connection to Reddit is functional.

The process is the same as the install stage but swap `npm start` for `npm test`.

See `.travis.yml` for more information.

<br>

### Install

Tested with `Python 3.7` and `Node v10` but earlier versions 'should' work - we don't use any bleeding edge features.

Set your Reddit API keys to enviroment values `CLIENTID` and `CLIENTSECRET`.

`pip install -r requirements.txt`

`npm install`

`npm start`

The project is then hosted on `localhost`, the port is `PORT` or 8080.
