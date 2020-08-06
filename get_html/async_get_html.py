import asyncio
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import BasicAuth
import json
import time


async def fetch(url, referer, session):
    timeout = ClientTimeout(total=200)

    async with session.get(url, timeout=timeout, proxy=proxy, proxy_auth=proxy_auth, headers=useragent(referer)) as response:
        response = json.loads(await response.read())
        return response


async def run(urls):
    tasks = []
    async with ClientSession() as session:
        for url, referer in urls:
            task = asyncio.ensure_future(fetch(url, referer, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        return await responses



def get_htmls(urls):
    result = []
    step = 20
    print(f'ссылок: {len(urls)}')
    while urls:
        step_urls = urls[:step]
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(step_urls))
        _ = [result.extend(i) for i in loop.run_until_complete(future) if i]
        urls = urls[step:]
        time.sleep(1)

    return result


proxy_auth = BasicAuth('tuthixen-dest', '53d8tl329rrx')

def useragent(referer):
    return {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'accept': 'application/json',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json', 'origin': 'https://www.pinnacle.com', 'referer': f'{referer}',
        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
        'x-api-key': 'CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R',
        'x-device-uuid': '09c6ce18-862b2b94-6ffb6791-798ca959'}

with open('../get_html/proxies.txt', 'r') as file:
    proxies = file.read().split('\n')


proxy = "http://tuthixen-dest:53d8tl329rrx@23.236.187.108:80"

# document.write_lines('test2ip.html', get_htmls(['https://2ip.ru/','https://2ip.ru/','https://2ip.ru/','https://2ip.ru/','https://2ip.ru/',]), 'w')
