import asyncio
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import BasicAuth
import json
import time
from document import document
from Session.Token import Token



async def fetch(url, referer, session):
    proxy_auth = BasicAuth('tuthixen-dest', '53d8tl329rrx')
    proxy = f"http://{user_headers[-2]}"
    try:
        timeout = ClientTimeout(total=30, connect=15, sock_connect=15, sock_read=15)
        async with session.get(url, timeout=timeout, proxy=proxy, proxy_auth=proxy_auth, headers=useragent(referer, user_headers)) as response:
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
    global user_headers
    user_headers = Token().get_token()
    urls = urls if isinstance(urls, list) else [urls]
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


def useragent(referer, user_headers):
    referer = referer.replace('e-s', 'es')
    return {
        'User-Agent': f'{user_headers[2]}',
        'accept': 'application/json',
        'accept-language': 'en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json', 'origin': 'https://www.pinnacle.com', 'referer': f'{referer}',
        'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
        'x-api-key': f'{user_headers[0]}',
        'x-device-uuid': f'{user_headers[1]}'}