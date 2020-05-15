import requests
import json

from conf import *

URL = MY_URL


def get_list():
    count = 1
    urls = []
    while True:
        try:
            data = requests.get(URL.format(count), headers=HEADERS)
            content = json.loads(data.content)
            vlist = content.get('data').get('list').get('vlist')
            aid_list = [item.get('aid') for item in vlist]
            if not aid_list:
                return urls
            urls += ['https://www.bilibili.com/video/av' + str(item) for item in aid_list]
            # print('播放列表抓取了{}页'.format(count))
            count += 1

        except Exception as e:  # 抓到报错为止
            return urls


if __name__ == '__main__':
    import os
    os.chdir('../')
    aa = get_list()

