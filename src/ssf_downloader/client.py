import re
import json
import hashlib
import aiohttp
import cloudscraper
from bs4 import BeautifulSoup
from typing import Self, Optional
from models import UserInfo, FileDetails

class SSFClient:
    BASE_URL = 'https://api.77drive.com/'

    def __init__(
        self,
        username=None,
        password=None,
        device_id=None
    ):
        self.username = username
        self.password = password
        self.device_id = device_id
        self.user_info = None
        self._scraper = cloudscraper.create_scraper()
        self._http_client = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    def _md5(self, string):
        return hashlib.md5(string.encode()).hexdigest()

    def _get_wap_url(self, url):
        pattern = '[https\:\/\/www\.]?77file\.com\/s\/(.*?)'

        if re.match(pattern, url):
            return f"https://www.77file.com/wap.php?action=view&s={url.split('/')[-1]}"
        return url

    def _get_file_id(self, url):
        pattern = "location\.href\=\'share77file\:\/\/share\?fileid\=(.*?)\&key\=(.*?)\'"

        text = self._scraper.get(url).text
        html = BeautifulSoup(text, 'lxml')

        element = html.find(
            'button',
            dict(id='appdown-link')
        ).attrs['onclick']
        match = re.match(pattern, element)

        if match:
            return match[1], match[2]

    async def close(self):
        await self._http_client.close()

    def register(self, username, email, password):
        return self._scraper.post(
            'https://www.77file.com/wap_ajax.php',
            data=dict(
                action='doregister',
                u=username,
                p=password,
                p2=password,
                e=email,
                q='',
                c=''
            ),
        ).text

    async def login(self, username=None, password=None):
        if username and password:
            self.username = username
            self.password = password

        async with self._http_client.post(
            f'{self.BASE_URL}/api/userinfo.php',
            data=dict(
                username=self.username,
                passwd=self._md5(self.password),
                login='1',
                agent=self.device_id
            )
        ) as response:
            json_string = await response.text()
            self.user_info = UserInfo(**json.loads(json_string)[0])

    async def get_file_details(self, url):
        new_url = self._get_wap_url(url)
        file_id = self._get_file_id(new_url)[0]

        async with self._http_client.post(
            f'{self.BASE_URL}/api/apidown.php',
            data=dict(
                fileid=file_id,
                down_key=self._md5(f'{file_id}downvawsvnopwqv'),
                passwd=self._md5(self.password),
                uid=self.user_info.userid,
                agent=self.device_id
            )
        ) as response:
            json_string = await response.text()
            return FileDetails(**json.loads(json_string)[0])