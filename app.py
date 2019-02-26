import websockets
import asyncio
import json
import praw

with open('emojis/emoji.json', encoding='utf8') as emoji_db:
    cleaned = filter(lambda e: 'emoji' in e, json.load(emoji_db))
    emojis = set(map(lambda e: e['emoji'], cleaned))

reddit = praw.Reddit(client_id='x',
                     client_secret='x',
                     user_agent='emoji-tracker v0')


connected = set()


async def register(websocket):
    connected.add(websocket)


async def unregister(websocket):
    connected.remove(websocket)


async def receiver(websocket, path):
    await register(websocket)


async def send_emojis(emojis):
    print('send emojis')
    print(str(connected))
    for client in connected:
        try:
            await client.send(emojis)
        except:
            await unregister(client)
    await scan_emojis()


async def scan_emojis():
    recent_emojis = list()
    for comment in reddit.subreddit('all').stream.comments(pause_after=-1):
        if comment is None:
            return await send_emojis(''.join(recent_emojis))
        for char in comment.body:
            if char in emojis:
                recent_emojis.append(char)

async def main(websocket, path):
    await register(websocket)
    await scan_emojis()


asyncio.get_event_loop().run_until_complete(
    websockets.serve(main, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
