from web_utils import *
from bs4 import BeautifulSoup
import asyncio
from urllib.parse import urlparse

START_URL = r'https://www.bh3.com/valkyries'


async def main():
    html = get_html(START_URL)
    info = urlparse(START_URL)
    host = info.scheme + '://' + info.netloc
    soup = BeautifulSoup(html, 'html.parser')
    tasks = []
    results = []
    for box in soup.div(class_='base-role-btn'):
        url = host + box.parent['href']
        tasks.append(asyncio.create_task(get_valkyire_info(url, results)))
    await asyncio.gather(*tasks)

    results.sort(key=lambda r: r[1])
    with open('Valkyrie Data.txt', 'w', encoding='utf-8') as f:
        for armor, name, birth, method in results:
            f.write(f'{name}\t{armor}\t{birth}\t{method}\n')


async def get_valkyire_info(url, results):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    info = soup.div(class_='valkyries-detail-bd__card')[0].div()
    armor = info[0].string.strip()
    name = info[2].string.strip()[3:]
    birth = info[3].string.strip()[3:]
    method = info[5].string.strip()[5:]
    results.append([armor, name, birth, method])


if __name__ == "__main__":
    asyncio.run(main())