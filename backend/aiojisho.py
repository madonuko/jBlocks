#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from json.decoder import JSONDecodeError

import aiohttp

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class APIException(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class Client:
    DOMAIN = 'jisho.org'
    VERSION = 1

    def __init__(self):
        base_url = f'https://{Client.DOMAIN}/api/v{Client.VERSION}'
        self._base_url = base_url

    @staticmethod
    def clean_params(params):
        return {k: v for k, v in params.items() if v is not None}

    async def _get(self, url, params=None):
        if params is None:
            params = {}

        params = self.clean_params(params)

        logger.debug(url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                try:
                    if res.status != 200:
                        raise APIException(
                            res.status,
                            res.content.decode()
                        )

                    json = await res.json()
                    return json
                except JSONDecodeError:
                    return res.content.decode()

    async def search(self, keyword):
        url = f'{self._base_url}/search/words'
        params = {'keyword': keyword} if keyword else {}
        return await self._get(url, params=params)
