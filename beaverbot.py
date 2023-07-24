import asyncio
import websockets
import requests
import json
import wshelper
import random

class DiscordClient:
    def __init__(self, token, whitelist=[]):
        wshelper.set_token(token)
        self.websocket = None
        self.events = {}
        self.ack_timeout = 1
        self.whitelist = whitelist
    
    async def start(self):
        self.websocket = await websockets.connect("wss://gateway.discord.gg/?v=10&encoding=json", max_size=5_000_000)
        await self.websocket.send(json.dumps(wshelper.HELLO))
        asyncio.create_task(self.heartbeat_loop())
        
        while True:
            try:
                message = json.loads(await self.websocket.recv())
                if message["op"] == 10:
                    self.ack_timeout = message["d"]["heartbeat_interval"] / 1000
                    print("[!] <3 => " + str(self.ack_timeout))
                if message["t"] in self.events:
                    if "guild_id" not in message["d"]:
                        continue
                    if message["d"]["guild_id"] not in self.whitelist:
                        continue
                    rand = random.randint(0, 50)
                    print(rand)
                    if rand != 25:
                        continue
                    for func in self.events[message["t"]]:
                        asyncio.create_task(func(message))
                        print("[!] Reply to " + message["d"]["author"]["username"] + ". Channel " + message["d"]["channel_id"])
            except Exception as ex:
                print(ex)
                break
    
    async def add_event(self, message, function):
        if not message in self.events:
            self.events[message] = []
        self.events[message].append(function)
    
    async def heartbeat_loop(self):
        HEARTBEAT = json.dumps(wshelper.HEARTBEAT)
        while True:
            await asyncio.sleep(self.ack_timeout)
            await self.websocket.send(HEARTBEAT)
            print("[!] <3")

http = requests.Session()
http.headers = {
    "Authorization": wshelper.BOT_TOKEN,
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Content-Type": "application/json"
}

async def handle_message(message):
    MESSAGE_REPLY = wshelper.http_create_reply(message, "https://tenor.com/view/beaver-hi-gif-21291049")
    url = "https://discord.com/api/v9/channels/" + MESSAGE_REPLY["message_reference"]["channel_id"] + "/messages"
    http.headers["Authorization"] = wshelper.BOT_TOKEN
    http.post(url, data=json.dumps(MESSAGE_REPLY))

async def main():
    client = DiscordClient("BOT_TOKEN", whitelist=[])
    await client.add_event("MESSAGE_CREATE", handle_message)
    await client.start()

if __name__ == '__main__':
    asyncio.run(main())
