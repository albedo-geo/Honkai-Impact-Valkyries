import requests

__all__ = ["HEADERS", "TIMEOUT", "get_html"]

HEADERS = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/68.0.3440.106 Safari/537.36',
    'accept-encoding':
    'gzip, deflate, br',
    'accept-language':
    'zh,en-US;q=0.9,en;q=0.8'
}
TIMEOUT = 8


def get_html(url):
    """获取给定 url 网址的 html 文档"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(f'Cannot access {url}. {e}')
        return ''