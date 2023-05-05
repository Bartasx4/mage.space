import json
import asyncio

from connection import Connection


class Tasker:
    GENERATE_URL = "https://api.mage.space/api/v3/images/generate"

    def __init__(self, connection: Connection):
        self.connection = connection

    async def download(self, url: str):
        ...

    async def start_loop(self, request):
        tasks = []
        for item in request:
            tasks.append(asyncio.create_task(self.connection.get(self.GENERATE_URL, get=False, data=item)))
        result = await asyncio.gather(*tasks)
        for item in result:
            code, response = item
            if code == 200:
                response = json.loads(response)['results'][0]
                print(f'{response["is_nsfw"]=}, {response["is_public"]=}, {response["is_enhanced"]=}')
            else:
                print(item)
