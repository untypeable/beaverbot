import asyncio
import json
import random

import websockets
import requests

import wsconfig

FISHPOND = "592887581402988563"
BOT_TESTING = "886339210360021072"

BEAVERS = [
    "https://tenor.com/view/beaver-beaver-walk-beaver-hug-gif-3230734869832725232",
    "https://tenor.com/view/beaver-hi-gif-21291049",
    "https://tenor.com/view/beaver-carrot-eating-gif-21665554",
    "https://tenor.com/view/beaver-carrying-hurry-%D0%B1%D0%BE%D0%B1%D0%B5%D1%80-carrots-gif-25255221",
    "https://tenor.com/view/look-anyway-eating-chewing-beaver-gif-11989160466131802631",
    "https://tenor.com/view/groundhog-groundhog-eating-wait-gif-3478318557675834878"
]

class BeaverBot:
    def __init__(self):
        self.client: websockets.ClientConnection = None
        self.interval: int = 40
        self.running: bool = False
        self.whitelist: any = [FISHPOND,BOT_TESTING]
        self.sequence: int = 0
        self.heartbeat: asyncio.Task = None
    
    async def connect(self):
        self.client = await websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=5_000_000)
        await self.client.send(wsconfig.WS_HELLO)
        self.running = True
        self.heartbeat = asyncio.create_task(self.heartbeat_loop())
    
    async def reconnect(self):
        self.heartbeat.cancel()
        await self.client.close()
        await self.connect()
    
    async def send_heartbeat(self):
        wsconfig.ws_sequence(self.sequence)
        await self.client.send(wsconfig.WS_HEARTBEAT)
        print(f"Heartbeat, {self.sequence}")
    
    async def heartbeat_loop(self):
        while self.running:
            await asyncio.sleep(self.interval)
            await self.send_heartbeat()
    
    async def start(self):
        while self.running:
            message = await self.client.recv()
            try:
                data: any = json.loads(message)
                
                op: int = data["op"]
                t: str = data["t"]
                d: any  = data["d"]
                s: any = data["s"]

                print(f"OP: {op}")

                match op:
                    case 1:
                        self.send_heartbeat()
                    case 7:
                        await self.reconnect()
                    case 9:
                        await self.reconnect()
                    case 10:
                        self.interval = d["heartbeat_interval"] / 1000
                
                if s: self.sequence = s

                if "author" in d and d["author"]["id"] == "1385049954816495686":
                    continue
                
                if t == "MESSAGE_CREATE":
                    if d["guild_id"] not in self.whitelist: continue
                    self.handle_message(d)
                    print(d["author"]["id"])

            except Exception as ex:
                print(message)
                print(ex)
        self.running = False
    
    def handle_message(self, data: any):
        content: str = data["content"]
        if content.startswith("!bb"):
            wsconfig.http_reply(data, random.choice(BEAVERS))
            return
        rand: int = random.randint(0, 30)
        if rand == 15:
            wsconfig.http_reply(data, random.choice(BEAVERS))

async def main():
    bot = BeaverBot()
    await bot.connect()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
