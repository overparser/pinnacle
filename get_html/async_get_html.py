import asyncio
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import BasicAuth
import json
import time
from document import document

async def fetch(url, referer, session):
    proxy_auth = BasicAuth('tuthixen-dest', '53d8tl329rrx')
    proxy = "http://tuthixen-dest:53d8tl329rrx@45.137.40.144:80"
    try:
        timeout = ClientTimeout(total=30, connect=15, sock_connect=15, sock_read=15)
        async with session.get(url, timeout=timeout, proxy=proxy, proxy_auth=proxy_auth, headers=useragent(referer)) as response:
            response = json.loads(await response.read())
            return response
    except:
        return []


async def run(urls):
    tasks = []
    async with ClientSession() as session:
        for url, referer in urls:
            task = asyncio.ensure_future(fetch(url, referer, session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        return await responses



def get_htmls(urls):
    urls = urls if isinstance(urls, list) else [urls]
    result = []
    step = 10
    print(f'ссылок: {len(urls)}')
    while urls:
        step_urls = urls[:step]
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(step_urls))
        _ = [result.extend(i) for i in loop.run_until_complete(future) if i]
        urls = urls[step:]
        time.sleep(1)

    return result

session_token = document.read_document('text_files/token.txt')
print(session_token, 'token')
def useragent(referer):
    referer = referer.replace('e-s', 'es')
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'accept': 'application/json',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json', 'origin': 'https://www.pinnacle.com', 'referer': f'{referer}',
        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
        'x-api-key': 'CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R',
        'x-device-uuid': 'f908df91-3a2e2367-33f7c582-961e96a5',
        'x-session': session_token}