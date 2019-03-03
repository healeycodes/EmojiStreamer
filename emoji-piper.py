''' @healeycodes
EmojiStreamer - pipe emoji to stdout live from Reddit comments
'''
import os
import sys
import json
import praw
sys.stdout.reconfigure(encoding='utf-8')

with open('emojis/emoji.json', encoding='utf8') as emoji_db:
    cleaned = filter(lambda e: 'emoji' in e, json.load(emoji_db))
    emojis = set(map(lambda e: e['emoji'], cleaned))

client_id = os.environ['CLIENTID']
client_secret = os.environ['CLIENTSECRET']
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='emoji-tracker v0')

while True:
    try:
        for comment in reddit.subreddit('all').stream.comments():
            for char in comment.body:
                if char in emojis:
                    print(char, flush=True)
    except Exception as e:
        print(e, file=sys.stderr)
