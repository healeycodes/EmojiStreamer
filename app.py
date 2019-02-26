import websockets
import asyncio
import json
import praw


class EmojiStreamer():
    def __init__(self, emojis, client_id, client_secret):
        self.emojis = emojis
        self.reddit = self.get_reddit(client_id, client_secret)
        self.clients = set()

    def get_reddit(self, client_id, client_secret):
        return praw.Reddit(client_id=client_id,
                           client_secret=client_secret,
                           user_agent='emoji-tracker v0')

    async def register(self, websocket):
        self.clients.add(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def send_emojis(self, emojis):
        for client in self.clients:
            try:
                await client.send(emojis)
            except:
                await self.unregister(client)
        await self.scan_emojis()

    async def scan_emojis(self):
        recent_emojis = list()
        for comment in self.reddit.subreddit('all').stream.comments(pause_after=-1): #TODO: emojis might be sent more than once, use dblqueue?
            if comment is None:
                if len(recent_emojis) > 1:
                    return await self.send_emojis(''.join(recent_emojis))
                await self.scan_emojis()
            for char in comment.body:
                if char in self.emojis:
                    recent_emojis.append(char)

    async def main(self, websocket, path):
        await self.register(websocket)
        await self.scan_emojis()


with open('emojis/emoji.json', encoding='utf8') as emoji_db:
    cleaned = filter(lambda e: 'emoji' in e, json.load(emoji_db))
    emojis = set(map(lambda e: e['emoji'], cleaned))

emoji_streamer = EmojiStreamer(
    emojis, 'x', 'x')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(emoji_streamer.main, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
