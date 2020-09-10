import asyncio
from aiohttp import ClientSession
from aiohttp import ClientTimeout
from aiohttp import BasicAuth
import json
import time
from document import document
from Session.Token import Token


async def fetch(url, referer, session, user_headers):
    proxy_auth = BasicAuth('tuthixen-dest', '53d8tl329rrx')
    proxy = f"http://{user_headers[-2]}"
    try:
        timeout = ClientTimeout(total=30, connect=15, sock_connect=15, sock_read=15)
        async with session.get(
                url,
                timeout=timeout,
                proxy=proxy,
                proxy_auth=proxy_auth,
                headers=useragent(referer, user_headers)) as response:
            response = json.loads(await response.read())
            return response
    except:
        return []

async def bound_fetch(url, referer, sem, user_headers):
    async with ClientSession() as session:
        async with sem:
            return await fetch(url, referer, session, user_headers)

def get_objects_from_list_of_tuples(urls: list) -> list:
    """takes list of tuples (url, referer) and does async requests :returns list of objects"""
    user_headers = Token().get_token()
    urls = urls if isinstance(urls, list) else [urls]
    sem = asyncio.Semaphore(2)
    print(f'ссылок: {len(urls)}')
    loop = asyncio.get_event_loop()
    futures = []
    response_list = []
    for url, referer in urls:
        futures.append(asyncio.ensure_future(bound_fetch(url, referer, sem, user_headers)))
    for elem in map(loop.run_until_complete, futures):
        response_list.extend(elem)
    return response_list


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