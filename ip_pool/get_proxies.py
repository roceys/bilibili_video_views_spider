import os
import time
import re
import csv
from threading import Thread
import requests
import fake_useragent
from ip_pool import api_settings
from ip_pool.csv_helper import get_random_ip_in_pool


class ProxiesSpider:
    def __init__(self):
        self.url = api_settings.URL_MAIN
        self.url2 = api_settings.URL_TEST
        self.count = 0

    def get_html(self):
        for i in range(1, 3423):
            url = self.url.format(i)
            headers = {'User-Agent': fake_useragent.UserAgent().random}

            try:
                proxies = self.get_random_proxy()
                if api_settings.USE_PROXY:
                    res = requests.get(url,
                                       headers=headers,
                                       timeout=api_settings.TIME_OUT,
                                       proxies=proxies
                                       )
                else:
                    res = requests.get(url,
                                       headers=headers,
                                       timeout=api_settings.TIME_OUT,
                                       )
            except Exception as e:
                print(e)
                continue
            res.encoding = 'utf-8'
            html = res.content
            self.parse_html(html)
            print('第{}页抓取完成,休眠2秒,抓取下一页.....'.format(i))

    @staticmethod
    def get_random_proxy():
        ip = 'http://' + get_random_ip_in_pool()
        proxies = {
            'http': ip,
            'https': ip,
        }
        return proxies

    def parse_html(self, html):
        html = html.decode()
        pattern = re.compile(r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>', re.S)
        result_list = pattern.findall(html)
        # [('121.226.53.201', '61234'), ('120.83.97.81', '9999')......]

        r_list_addr = [tup[0] + ':' + tup[1] for tup in result_list]

        for i in range(len(r_list_addr)):
            self.count += 1
            t = Thread(target=self.test_html, args=(r_list_addr[i],))
            t.daemon = True
            time.sleep(api_settings.THREAD_DELTA)
            t.start()

    def test_html(self, addr):
        for i in range(3):
            try:
                # proxies = self.get_random_proxy()
                in_time = time.time()
                res = requests.get(self.url2,
                                   # proxies=proxies,
                                   timeout=api_settings.TIME_OUT)
                out_time = time.time()
                delta = out_time - in_time
                # if delta > 2:
                #     raise ValueError('响应时间过长')
                res.encoding = 'utf-8'
                print(res.text)
                if "httpbin.org/get" in res.text:
                    self.write_html(addr, delta)

            except Exception as e:
                print(addr + '第' + str(self.count) + "次连接失败")

    @staticmethod
    def write_html(addr, delta):
        if not os.path.exists(api_settings.FILE_NAME):
            open(api_settings.FILE_NAME, 'w')
        with open(api_settings.FILE_NAME, 'r') as f:
            reader = csv.reader(f)
            for item in reader:
                if addr in item:
                    print('>>>>>>>>>addr existed<<<<<<<<<<')
                    return
        with open(api_settings.FILE_NAME, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([addr, delta])
            f.flush()

    def run(self):
        self.get_html()


if __name__ == "__main__":
    s01 = ProxiesSpider()
    s01.run()
