import json
import requests
import wsmsg

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

def ws_heartbeat(sequence):
    data = HEARTBEAT.copy()
    data["d"]["s"] = sequence
    return json.dumps(data)

http = requests.Session()
http.headers = {
    "Authorization": f"Bot {BOT_TOKEN}",
    "Content-Type": "application/json",
}

def http_reply(message: wsmsg.Message, content):
    httpdata = HTTP_REPLY.copy()
    if message.guild_id: httpdata["message_reference"]["guild_id"] = message.guild_id
    httpdata["message_reference"]["channel_id"] = message.channel_id
    httpdata["message_reference"]["message_id"] = message.id
    httpdata["content"] = content
    url = "https://discord.com/api/v9/channels/" + message.channel_id + "/messages"
    req = http.post(url, data=json.dumps(httpdata))
    print(f"[+] HTTP REPLY {req.status_code} {url} {content}")
    return req