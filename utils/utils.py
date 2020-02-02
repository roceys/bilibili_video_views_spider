import re
import requests


def get_bilibili_play_times(url):
    # url = 'https://www.bilibili.com/video/av20379071/'
    headers = {
        # 'Accept': 'application/json, text/plain, */*',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cache-Control': 'no-cache',
        # 'Connection': 'keep-alive',
        # 'Host': 'api.bilibili.com',
        # 'Origin': 'https://space.bilibili.com',
        # 'Pragma': 'no-cache',
        # 'Referer': 'https://space.bilibili.com/10241912/video',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    re_str = '"viewseo":(\d*)'
    result = re.findall(re_str, res.text)
    times = result[0] if result else None
    return times

