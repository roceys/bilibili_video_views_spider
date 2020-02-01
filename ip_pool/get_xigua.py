import os
from threading import Thread
import requests
from ip_pool import api_settings
from ip_pool.get_proxies import ProxiesSpider

res = requests.get(api_settings.XIGUA_URL,headers = api_settings.XG_HEADERS)
res = res.text.split('\r\n')


class XiGua(ProxiesSpider):

    def main(self):
        # with open('proxies', 'r') as f:
        #     rows = f.readlines()
        if os.path.exists(api_settings.FILE_NAME):
            os.remove(api_settings.FILE_NAME)
        rows = res
        t_list = []
        for addr in rows:
            addr = addr.strip()
            t = Thread(target=self.test_html, args=(addr,))
            t.start()
            t_list.append(t)
        for t in t_list:
            t.join()

if __name__ == '__main__':
    x01 = XiGua()
    x01.main()
