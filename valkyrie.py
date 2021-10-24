import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re
import asyncio
from web_utils import *


async def get_pic(url, path):
    """将网址对应图片保存到本地指定位置"""
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    if r.status_code == 200:
        with path.open('wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        print(f'Cannot download {url}')


async def download_mt(imgs_to_dl):
    """异步下载所有图片到本地"""
    tasks = []
    for src, file in imgs_to_dl:
        task = asyncio.create_task(get_pic(src, file))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def main():
    home = 'https://www.bh3.com'
    folder = Path('Valkyries')
    if not folder.exists():
        folder.mkdir()

    html = get_html(home + '/valkyries')
    soup = BeautifulSoup(html, 'html.parser')
    avatar_list = soup.find('div', class_="valkyries-item")

    imgs_to_dl = []

    for a in avatar_list.find_all('a', href=re.compile(r'/valkyries/\d+/\d+')):
        page = get_html(home + a['href'])
        _soup = BeautifulSoup(page, 'html.parser')
        name = _soup.find('div', class_='name').text.strip()
        saveas = folder / name

        print(name)
        if saveas.exists():
            continue

        src = _soup.find('div', class_='big-img').img['src']

        imgs_to_dl.append((src, saveas.with_suffix('.png')))

    await download_mt(imgs_to_dl)
    print("下载完毕")


if __name__ == '__main__':
    asyncio.run(main())
