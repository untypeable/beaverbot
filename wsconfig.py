import json
import requests

BOT_TOKEN = ""

HELLO = {
   "op": 2,
   "d": {
      "token": BOT_TOKEN,
      "intents": 33280,
      "properties": {
         "os": "TempleOS",
         "browser": "HolyBrowser",
         "device": "ComputerOfGod"
      },
      "compress": False,
   }
}

HEARTBEAT = {
    "op": 1,
    "d": {
        "token": BOT_TOKEN,
        "properties": {
            "os": "TempleOS",
            "browser": "HolyBrowser",
            "device": "ComputerOfGod"
        },
    }
}

HTTP_REPLY = {
    "content": "",
    "nonce": None,
    "tts": False,
    "message_reference":{
    },
    "allowed_mentions":{
        "parse":[
            "users",
            "roles",
            "everyone"
            ],
        "replied_user": True
    },
    "flags":0
}

WS_HELLO = json.dumps(HELLO)
WS_HEARTBEAT = json.dumps(HEARTBEAT)

def ws_sequence(sequence):
    global HEARTBEAT, WS_HEARTBEAT
    HEARTBEAT["d"]["s"] = sequence
    WS_HEARTBEAT = json.dumps(HEARTBEAT)

http = requests.Session()
http.headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    #"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
    "Content-Type": "application/json",
    #"Origin": "https://discord.com",
    #"Referer": "https://discord.com/channels/886339210360021072/886339210360021075"
}

def http_reply(data, content):
    reply = HTTP_REPLY.copy()
    if "guild_id" in data:
        reply["message_reference"]["guild_id"] = data["guild_id"]
    reply["message_reference"]["channel_id"] = data["channel_id"]
    reply["message_reference"]["message_id"] = data["id"]
    reply["content"] = content

    url = "https://discord.com/api/v9/channels/" + data["channel_id"] + "/messages"
    req = http.post(url, data=json.dumps(reply))
    print(f"REPLY {req.status_code} {url} {content}")

    return req