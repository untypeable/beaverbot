import asyncio
import json
import random

import wsmsg
import wsconfig

import beaverbot

BEAVERS = [
    "https://tenor.com/view/beaver-beaver-walk-beaver-hug-gif-3230734869832725232",
    "https://tenor.com/view/beaver-hi-gif-21291049",
    "https://tenor.com/view/beaver-carrying-hurry-%D0%B1%D0%BE%D0%B1%D0%B5%D1%80-carrots-gif-25255221",
    "https://tenor.com/view/beaver-carrot-eating-gif-21665554",
    "https://tenor.com/view/marmot-stupid-marmot-gif-18279475216139709294",
    "https://tenor.com/view/koharu-bunny-eating-munching-bunny-munching-gif-14734225609698921002",
    "https://tenor.com/view/bunny-cute-bun-rabbit-dance-gif-12204421675478327501",
    "https://tenor.com/view/bunny-sleepy-gooba-owa-owaowa-gif-2311503198775714764",
    "https://tenor.com/view/bunny-rabbit-angry-attack-gif-8318612315233716848",
    "https://tenor.com/view/bunny-bunny-carry-carrying-away-bunny-bunny-walk-chill-bunny-gif-718057308746791294",
    "https://tenor.com/view/jeg-k%C3%B8rer-go-home-son-gif-20042658",
    "https://tenor.com/view/katturide-gif-27002722",
    "https://tenor.com/view/capibara-gif-22235175",
    "https://tenor.com/view/capy-turtule-capybara-uber-gif-26711606",
    "https://tenor.com/view/capybara-gif-26095126",
    "https://tenor.com/view/guinea-pig-me-when-i-get-you-gif-26070933",
    "https://tenor.com/view/guinea-pig-gif-26738228",
    "https://tenor.com/view/hamster-wut-what-shocked-sad-gif-14800788176891041699"
]

async def beaverchance(data: wsmsg.Message):
    rand: int = random.randint(0, 30)
    if rand == 1:
        wsconfig.http_reply(data, random.choice(BEAVERS))

async def bb(data: wsmsg.Message):
    if data.content.startswith("!bb"):
        wsconfig.http_reply(data, random.choice(BEAVERS))

async def test(data: wsmsg.Message):
    if data.content.startswith("!test"):
        wsconfig.http_reply(data, "Test")

async def main():
    bot = beaverbot.BeaverBot()
    events = [beaverchance, bb, test]
    bot.events["MESSAGE_CREATE"] = events
    await bot.connect()
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())