import websockets
import wsconfig
import wsmsg
import asyncio
import json

FISHPOND = ""
BOT_TESTING = ""
SERVER_WHITELIST = [FISHPOND,BOT_TESTING]
USER_BLACKLIST = ["",""]

class BeaverBot:
    def __init__(self):
        self.client: websockets.ClientConnection = None
        self.interval: int = 40
        self.running: bool = False
        self.sequence: int = 0
        self.heartbeat: asyncio.Task = None
        self.events: dict = {}
    
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
        data = wsconfig.ws_heartbeat(self.sequence)
        await self.client.send(data)
        print(f"[+] Heartbeat {self.sequence}")
    
    async def heartbeat_loop(self):
        while self.running:
            await asyncio.sleep(self.interval)
            await self.send_heartbeat()
    
    async def core_loop(self):
        while self.running:
            try:
                recv = await self.client.recv()
                data = json.loads(recv)
                meta = wsmsg.Meta(data)
                match meta.op:
                    case 1:
                        self.send_heartbeat()
                    case 7:
                        await self.reconnect()
                    case 9:
                        await self.reconnect()
                    case 10:
                        self.interval = meta.d["heartbeat_interval"] / 1000
                if meta.s: self.sequence = meta.s
                if meta.t == "MESSAGE_CREATE":
                    message = wsmsg.Message(meta)
                    if message.guild_id not in SERVER_WHITELIST: continue
                    if message.author.id in USER_BLACKLIST: continue
                    await self.handle_message(message)
                    print(meta.op, meta.t, meta.s)
            except Exception as ex:
                await self.reconnect()
                print(recv)
                print(ex)
    
    async def start(self):
        while self.running:
            try:
                await self.reconnect()
                await self.core_loop()
            except Exception as ex:
                print("[!] Core Loop Error")
                print(ex)
    
    async def handle_message(self, data: wsmsg.Message):
        meta: wsmsg.Meta = data.meta
        events: list = self.events.get(meta.t)
        if events:
            for event in events:
                try:
                    await event(data)
                except Exception as ex:
                    print("[+] User Event Exception")
                    print(ex)
