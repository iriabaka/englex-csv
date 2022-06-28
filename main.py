import asyncio
import itertools
import os
import re
import sys
from dataclasses import dataclass
from urllib.parse import unquote_plus

import aiocsv
import aiofiles
import aiohttp

CSV_FILE = (sys.argv[1:2] or ('englex.csv',))[0]
USER_EMAIL = os.environ['ENGLEX_USER_EMAIL']
USER_PASSWORD = os.environ['ENGLEX_USER_PASSWORD']


class EnglexError(Exception):
    pass


@dataclass
class User:
    user_id: int
    auth_token: str


async def get_user(email: str, password: str, session: aiohttp.ClientSession) -> User:
    async with session.get('https://my.englex.ru/login') as resp:
        raw_cookie = unquote_plus(resp.cookies['YUPE_TOKEN'].value)
        csrf_token = re.search(r'"([^"]+)"', raw_cookie).group()

    async with session.post('https://my.englex.ru/login', data={
        'YUPE_TOKEN': csrf_token,
        'LoginForm[email]': email,
        'LoginForm[password]': password,
        'LoginForm[remember_me]': '0',
        'login-btn': ''
    }) as resp:
        if 'Email или пароль введены неверно!' in await resp.text():
            raise EnglexError('Email or password is incorrect!')

    async with session.get('https://my.englex.ru/student/studentTeacher/vc') as resp:
        refresh_token = resp.url.name

    async with session.post('https://api-class.englex.ru/v1/user/login', data={'token': refresh_token}) as resp:
        data = await resp.json()

    return User(user_id=data['user']['id'], auth_token=data['user']['token'])


async def get_words(dict_id: str, session: aiohttp.ClientSession) -> list[tuple[str, str]]:
    async with session.get(f'https://api-class.englex.ru/v2/dictionary-list/{dict_id}',
                           params={'expand': ['entryInstances']}) as resp:
        data = (await resp.json())['entryInstances']
        words = [(i['dictionaryEntry']['original'], i['dictionaryEntry']['translation']) for i in data]

        return words


async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        user = await get_user(USER_EMAIL, USER_PASSWORD, session)
        session.headers.add('Authorization', f'Bearer {user.auth_token}')

        async with session.get(f'https://api-class.englex.ru/v2/dictionary-instance/student/{user.user_id}/list') as r:
            dict_ids = [i['id'] for i in await r.json()]

        words = await asyncio.gather(*[get_words(dict_id, session) for dict_id in dict_ids])
        words = list(itertools.chain(*words))

        async with aiofiles.open(CSV_FILE, mode='w', encoding='UTF-8', newline='') as file:
            writer = aiocsv.AsyncWriter(file, delimiter='\t')
            await writer.writerows(words)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
