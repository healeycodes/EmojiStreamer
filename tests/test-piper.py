''' @healeycodes
test-piper.py - testing apparatus, mimics emoji-piper.py by piping out 10 emojis
'''
import os
import sys
import json
import random
sys.stdout.reconfigure(encoding='utf-8')

with open('emojis/emoji.json', encoding='utf8') as emoji_db:
    cleaned = filter(lambda e: 'emoji' in e, json.load(emoji_db))
    emojis = set(map(lambda e: e['emoji'], cleaned))

for i in range(10):
    rnd_emoji = random.sample(emojis, 1)[0]
    print(rnd_emoji, flush=True)
