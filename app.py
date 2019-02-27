import collections
import json
import asyncio
import websockets
import praw


class BoundedSet():
    def __init__(self, size):
        self.size = size
        self.store = set()
        self.fifo = collections.deque()

    def add(self, item):
        self.store.add(item)
        self.fifo.appendleft(item)
        if len(self.fifo) > self.size:
            self.store.remove(self.fifo.pop())

    def has(self, item):
        return item in self.store


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
        if len(self.clients) == 1:
            await self.scan_emojis()

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
        seen = BoundedSet(100)  # praw api can be unreliable
        while True:
            for comment in self.reddit.subreddit('all').stream.comments():
                if seen.has(comment.id):
                    continue
                else:
                    seen.add(comment.id)

                emojis = list()
                for char in comment.body:
                    if char in self.emojis:
                        emojis.append(char)
                if emojis:
                    await self.send_emojis(''.join(emojis))
                if len(self.clients) == 0:
                    return

    async def main(self, websocket, path):
        await self.register(websocket)


with open('emojis/emoji.json', encoding='utf8') as emoji_db:
    cleaned = filter(lambda e: 'emoji' in e, json.load(emoji_db))
    emojis = set(map(lambda e: e['emoji'], cleaned))

emoji_streamer = EmojiStreamer(
    emojis, 'x', 'x')

asyncio.get_event_loop().run_until_complete(
    websockets.serve(emoji_streamer.main, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
