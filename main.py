import asyncio
import json

import aiohttp

from requestdata import RequestData
from tasker import Tasker
from photo import Photo
from connection import Connection

MODELS = ['urpm',
          'realistic-vision-v2',
          'realistic-vision',
          'v2.1',  # Stable Diffusion 2.1
          ]

RATIO = {1.7777777777777777: '16:9',
         1.5: '3:2',
         0.6666666666666666: '2:3',
         0.5625: '9:16',
         1: '1'}

SUMMARY_URL = 'https://api.mage.space/api/v1/notifications/summary'
prompt = ""
negative_prompt = ""


daty = {"prompt": prompt,
        "aspect_ratio": 1,
        "num_inference_steps": 100,
        "guidance_scale": 9.5,
        "is_public": 'false',
        "easy_mode": 'false',
        "strength": 0.8,
        "model": "urpm",
        "seed": '',
        "negative_prompt": negative_prompt}


async def start():
    data = RequestData(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=85, model='urpm')
    async with aiohttp.ClientSession() as session:
        connection = Connection(session)
        connection.import_cookies()
        code, response = await connection.get(SUMMARY_URL)
        if code == 401:
            await connection.login()
        code, response = await connection.get('https://api.mage.space/api/v1/users/Bartek/creations?page=0&limit=1')
        last = Photo(json.loads(response))
        print(code, last())
        tasker = Tasker(connection)
        await tasker.start_loop([last() for _ in range(5)])

asyncio.run(start())



# https://api.mage.space/api/v1/users/Bartek/creations?page=0&limit=300
# https://api.mage.space/api/v1/interactions/likes
# https://api.mage.space/api/v1/following
# https://api.mage.space/api/v1/interactions/bookmarks
# https://api.mage.space/api/v1/notifications/summary

# num_creations":702,"num_following":0,"num_followers":0},"lists"
# https://api.mage.space/api/v1/users/bDUWBsBSuGfk5S0WCM8UI5jTDYC2

# 200
# 401  {"detail":"Could not validate credentials"}
# 422  {"detail":[{"loc":["body","seed"],"msg":"value is not a valid integer","type":"type_error.integer"}]}
# key, token: AIzaSyAzUV2NNUOlLTL04jwmUw9oLhjteuv6Qr4
# https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=AIzaSyAzUV2NNUOlLTL04jwmUw9oLhjteuv6Qr4
