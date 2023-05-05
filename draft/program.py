import asyncio
import aiohttp
import pickle
import json

from pathlib import Path
from requestdata import RequestData


def import_cookies(session: aiohttp.ClientSession, raw_cookies):
    # session.cookie_jar.update_cookies([(key, value) for key, value in self.cookies.items()])
    temp_cookies = {}
    for element in raw_cookies:
        cookie = aiohttp.cookiejar.Morsel()
        cookie['expires'] = str(element['expiry'])
        cookie['path'] = element['path']
        cookie['domain'] = element['domain']
        cookie['secure'] = element['secure']
        cookie['httponly'] = element['httpOnly']
        cookie['samesite'] = element['sameSite']
        cookie.set(element['name'], element['value'], element['value'])
        temp_cookies[element['name']] = cookie
    session.cookie_jar.update_cookies(temp_cookies)


HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "dnt": "1",
        "accept-langage": "pl,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,sv;q=0.6",
        'authorization': ""}
GENERATE_URL = "https://api.mage.space/api/v3/images/generate"
HOME_URL = "https://www.mage.space/"
TOKEN = 'token.pkl'
prompt = ""
negative_prompt = ""


async def generate(data_to_send, session):
    json_data = json.dumps(data_to_send).encode('utf-8')
    async with session.post(GENERATE_URL, data=json_data, headers=HEADERS) as response:
        text = await response.text()
        code = response.status
        # if code == 200:
        # await self.download_photo(Photo(json.loads(text)), session)
        return response.text()


async def start(to_do):
    async with aiohttp.ClientSession() as session:
        import_cookies(session, cookies)
        tasks = []
        for item in to_do:
            tasks.append(asyncio.create_task(generate(item, session)))
        result = await asyncio.gather(*tasks)
    print(result)


with open(TOKEN, 'rb') as file:
    cookies, HEADERS = pickle.load(file)

data = RequestData(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=85, model='urpm')
asyncio.run(start([data() for _ in range(1)]))


# 200
# 401  {"detail":"Could not validate credentials"}
# 422  {"detail":[{"loc":["body","seed"],"msg":"value is not a valid integer","type":"type_error.integer"}]}
# https://api.mage.space/api/v1/notifications/summary
# key, token: AIzaSyAzUV2NNUOlLTL04jwmUw9oLhjteuv6Qr4
# https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=AIzaSyAzUV2NNUOlLTL04jwmUw9oLhjteuv6Qr4