import asyncio
import aiohttp
import pickle
import json
import logging

from requestdata import RequestData

logger = logging.getLogger('__test__')
logger.setLevel(logging.DEBUG)
logger.debug('START')


class Connection:
    def __init__(self, cookies=None, headers=None, home_url=None, generate_url=None):
        self.cookies = cookies if cookies else {}
        self.headers = headers if headers else {}
        self.home_url = home_url if home_url else 'https://icanhazip.com/'
        self.generate_url = generate_url if generate_url else 'https://icanhazip.com/'
        self.sleep = 3 if not generate_url else 0

    async def generate(self, data):
        json_data = json.dumps(data).encode('utf-8')
        async with aiohttp.ClientSession() as session:
            if self.cookies:
                self.import_cookies(session)
                ...
            await asyncio.sleep(self.sleep)
            async with session.post(self.generate_url, data=json_data, headers=self.headers) as response:
                text = await response.text()
                return text

    def import_cookies(self, session: aiohttp.ClientSession):
        # session.cookie_jar.update_cookies([(key, value) for key, value in self.cookies.items()])
        cookies = {}
        for element in self.cookies:
            cookie = aiohttp.cookiejar.Morsel()
            cookie['expires'] = str(element['expiry'])
            cookie['path'] = element['path']
            # cookie['comment'] = element['']
            cookie['domain'] = element['domain']
            # cookie['max-age'] = element['']
            cookie['secure'] = element['secure']
            cookie['httponly'] = element['httpOnly']
            # cookie['version'] = element['']
            cookie['samesite'] = element['sameSite']
            cookie.set(element['name'], element['value'], element['value'])
            cookies[element['name']] = cookie
        session.cookie_jar.update_cookies(cookies)
        # for cookie in cookies:
        # session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])


async def __main__(data1, data2):
    test = Connection(*token_data, url_home, url_generate)
    tasks = [asyncio.create_task(test.generate(data1)),
             asyncio.create_task(test.generate(data2))]
    result = await asyncio.gather(*tasks)
    print(result)


url_generate = "https://api.mage.space/api/v3/images/generate"
url_home = "https://www.mage.space/"
prompt = "RAW photo of young cute naked girl, full length, young, full body, extremely pale skin, no underwear, nipple bumps fabric, pretty cute feminine, messy dyed hair, ass, emo, eyeliner, blush, detailed face, lipstick, prismatic/infrared lighting, home, room, RAW, photo, analog style, depth of field, atmospheric, highly detailed, UHD, depth of field, both eyes the same, masterpiece, high resolution, ultra quality, 16K, skin pores, matte, detailed lips, skin texture, 8k UHD"
negative_prompt = "Ugly face, disfigured, conjoined twins, handicapped, deformed, amputated, crosseyed, blurry, elongated neck, Disney, claws, broken hands, broken fingers, bent, low resolution, text, logos, digital paint, jpeg artefacts, asymmetrical eyes, cropped, fake breasts, flat light, high gamma, extra nipples, underwear, bra, bra-straps, adult, cartoon, asian, 3d"
request_data1 = RequestData(prompt=prompt, negative_prompt=negative_prompt, num_inference_steps=75, model='urpm')
request_data2 = RequestData(prompt='full body naked girl, '+prompt, negative_prompt=negative_prompt, num_inference_steps=85, model='urpm')

with open('token.pkl', 'rb') as file:
    token_data = pickle.load(file)

asyncio.run(__main__(request_data1(), request_data2()))
