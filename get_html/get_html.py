import grequests
import requests
import document.document

userAgent = {'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)'}

with open('../get_html/proxies.txt', 'r') as file:
    proxies = list(set(file.read().split('\n')))



def get_proxy():
    proxy = proxies.pop(0)
    proxies.append(proxy)
    proxy = {
    "http": f"http://{proxy}",
    "https": f"https://{proxy}"
    }
    return proxy


def greq_html(urls):
    rs = (grequests.get(u, headers=userAgent, proxies=get_proxy()) for u in urls)
    return grequests.map(rs, size=4)

def get_html(url, session=requests, count=0):
    if count < 10:
        try:
            r = session.get(url, timeout=15, headers=userAgent, proxies=get_proxy())
        except:
            count += 1
            print('except get_html', count, url)
            return get_html(url, session=session, count=count)
    else:
        return

    return r