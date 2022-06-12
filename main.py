import asyncio
import itertools
import os
import sys

import aiocsv
import aiofiles
import aiohttp

CSV_FILE = sys.argv[1]
STUDENT_ID = os.environ['ENGLEX_STUDENT_ID']
TOKEN = os.environ['ENGLEX_TOKEN']


async def get_words(dict_id: str, session: aiohttp.ClientSession) -> list[tuple[str, str]]:
    async with session.get(f'https://api-class.englex.ru/v2/dictionary-list/{dict_id}',
                           params={'expand': ['entryInstances']}) as resp:
        data = (await resp.json())['entryInstances']
        words = [(i['dictionaryEntry']['original'], i['dictionaryEntry']['translation']) for i in data]

        return words


async def main():
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {TOKEN}'}, raise_for_status=True) as session:
        async with session.get(f'https://api-class.englex.ru/v2/dictionary-instance/student/{STUDENT_ID}/list') as resp:
            dict_ids = [i['id'] for i in await resp.json()]

        words = await asyncio.gather(*[get_words(dict_id, session) for dict_id in dict_ids])
        words = list(itertools.chain(*words))

        async with aiofiles.open(CSV_FILE, mode='w', encoding='UTF-8', newline='') as file:
            writer = aiocsv.AsyncWriter(file, delimiter='\t')
            await writer.writerows(words)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
