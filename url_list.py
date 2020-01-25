import settings
import requests
import json

URL = settings.MY_URL


def get_list():
    count = 1
    urls = []
    while True:
        try:
            data = requests.get(URL.format(count), headers=settings.HEADERS)
            content = json.loads(data.content)
            vlist = content.get('data').get('list').get('vlist')
            aid_list = [item.get('aid') for item in vlist]
            if not aid_list:
                return urls
            urls = ['https://www.bilibili.com/video/av' + str(item) for item in aid_list]
            print('播放列表抓取了{}页'.format(count))
            count += 1

        except:
            return urls


if __name__ == '__main__':
    url_list = get_list()
    a = 1
