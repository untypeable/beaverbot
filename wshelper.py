def set_token(token):
    global BOT_TOKEN
    global HELLO
    global HEARTBEAT

    BOT_TOKEN = token
    HELLO["d"]["token"] = token
    HEARTBEAT["d"]["token"] = token

BOT_TOKEN = ""

HELLO = {
   "op":2,
   "d":{
      "token": BOT_TOKEN,
      "capabilities":4093,
      "properties":{
         "client_build_number":175856,
         "client_event_source": None,
         "design_id":0
      },
      "compress": False,
   }
}

HEARTBEAT = {
    "op": 1,
    "d": {
        "token": BOT_TOKEN,
        "properties":{
            "client_build_number":175856,
            "client_event_source": None,
            "design_id":0
        },
    }
}

def http_create_reply(context, message):
    REPLY = HTTP_MESSAGE_REPLY.copy()
    
    if "guild_id" in context["d"]:
        REPLY["message_reference"]["guild_id"] = context["d"]["guild_id"]
    
    REPLY["message_reference"]["channel_id"] = context["d"]["channel_id"]
    REPLY["message_reference"]["message_id"] = context["d"]["id"]
    REPLY["content"] = message
    
    return REPLY

HTTP_MESSAGE_REPLY = {
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
