import json
import pickle
import pathlib
import logging
import aiohttp
import undetected_chromedriver as uc

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from photo import Photo

logging.basicConfig(level=logging.INFO)


class Connection:
    HOME_URL = "https://www.mage.space/"
    TOKEN = 'token.pkl'
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "dnt": "1",
        "accept-langage": "pl,en;q=0.9,en-GB;q=0.8,en-US;q=0.7,sv;q=0.6",
        'authorization': ""
    }

    def __init__(self, session):
        # enable browser logging
        self._session = session
        self._d = DesiredCapabilities.CHROME
        self._d['goog:loggingPrefs'] = {'performance': 'ALL'}
        self._cookies = []
        if pathlib.Path(self.TOKEN).is_file():
            with open(self.TOKEN, 'rb') as file:
                self._cookies, self.HEADERS = pickle.load(file)

    async def login(self):
        self._cookies = []
        options = uc.ChromeOptions()
        options.add_argument('user-data-dir=selenium-profile')
        options.add_argument('--window-size=720,550')
        logging.debug('Opening browser.')
        with uc.Chrome(options=options, driver_executable_path='chromedriver.exe',
                       desired_capabilities=self._d) as driver:
            driver.set_window_size(720, 550)
            driver.get(self.HOME_URL)
            self._cookies = driver.get_cookies()
            logging.debug('Waiting for token and cookies.')
            while True:
                logs = str(driver.get_log('performance'))
                token = ''
                if 'Bearer' in logs:
                    start = logs.find('Bearer')
                    end = start + logs[start:].find('"')
                    token = logs[start:end]
                if self._cookies and token:
                    logging.info('Token: ' + str(token))
                    break
        logging.debug('Exiting browser.')
        driver.quit()
        self.HEADERS['authorization'] = token
        # str(a)[str(a).find('Bearer'):str(a).find('Bearer') + str(a)[str(a).find('Bearer'):].find('"')]
        with open(self.TOKEN, 'wb') as file:
            pickle.dump((self._cookies, self.HEADERS), file)

    async def generate(self, data):
        logging.debug('Generating...')
        json_data = json.dumps(data).encode('utf-8')
        async with self._session.post(self.GENERATE_URL, data=json_data, headers=self.HEADERS) as response:
            text = await response.text()
            code = response.status
            logging.debug(f'Response: ({str(code)}) {text}')
            # if code == 200:
            # await self.download_photo(Photo(json.loads(text)), session)
            return code, text

    async def get(self, url: str, get=True, data: dict[str: str | int] | None = None) -> tuple[int, str]:
        json_data = json.dumps(data).encode('utf-8') if data else ''
        if get:
            request = lambda: self._session.get(url, data=json_data, headers=self.HEADERS)
        else:
            request = lambda: self._session.post(url, data=json_data, headers=self.HEADERS)
        async with request() as response:
            text = await response.text()
            code = response.status
            return code, text

    def import_cookies(self):
        # session.cookie_jar.update_cookies([(key, value) for key, value in self.cookies.items()])
        cookies = {}
        for element in self._cookies:
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
        self._session.cookie_jar.update_cookies(cookies)

    async def download_photo(self, photo):
        logging.debug(f'Download: {photo.id}, {photo.url}')
        response = self._session.get(photo.url)
        with open('generated/' + photo.id + '.png', 'wb') as file:
            file.write(response.content)
