import sys
import logging
import json
import praw

with open('emojis/emoji.json', encoding='utf8') as emoji_db:
    cleaned = filter(lambda e: 'emoji' in e, json.load(emoji_db))
    emojis = set(map(lambda e: e['emoji'], cleaned))

client_id = sys.argv[1]
client_secret = sys.argv[2]
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent='emoji-tracker v0')

while True:
    try:
        for comment in reddit.subreddit('all').stream.comments():
            for char in comment.body:
                if char in emojis:
                    print(char)
    except Exception as e:
        logging.error(e)
