import os
import time
import re
import csv
from threading import Thread
import requests
import fake_useragent
from requests import ReadTimeout, ConnectTimeout
from requests.exceptions import ProxyError
from urllib3.exceptions import ConnectTimeoutError

from ip_pool import api_settings
from ip_pool.file_handler import get_random_ip_in_pool


class ProxiesSpider:
    def __init__(self):
        self.url = api_settings.URL_MAIN
        self.url2 = api_settings.URL_TEST
        self.count = 0

    def get_html(self):
        for i in range(1, 3423):
            print('开始一级爬取爬取,正在爬取第{}页'.format(i))
            url = self.url.format(i)
            headers = {'User-Agent': fake_useragent.UserAgent().random}

            try:
                if api_settings.USE_PROXY_TO_XICI:
                    proxies = self.get_random_proxy()
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

    @staticmethod
    def get_random_proxy():
        ip = get_random_ip_in_pool()
        proxies = {
            'http': 'http://' + ip,
            'https': 'https://' + ip,
        }
        return proxies

    def parse_html(self, html):
        print('正在解析...')
        html = html.decode()
        pattern = re.compile(r'<td>(\d+.\d+.\d+.\d+)</td>.*?<td>(\d+)</td>.*?<td>(HTTP.?)</td>', re.S)
        result_list = pattern.findall(html)
        list_addr = [tup[0] + ':' + tup[1] for tup in result_list]
        list_type = [tup[2].lower() for tup in result_list]
        for i in range(len(list_addr)):
            self.count += 1
            t = Thread(target=self.test_html, args=(list_addr[i], list_type[i]))
            t.daemon = True
            t.start()
            time.sleep(api_settings.THREAD_DELTA)

    def test_html(self, addr, type):
        for i in range(3):
            proxies = {
                'http': 'http://' + addr,
                'https': 'https://' + addr,
            }
            try:
                # print(proxies)
                in_time = time.time()
                res = requests.get(
                    self.url2,
                    timeout=api_settings.TIME_OUT,
                    proxies=proxies)
                out_time = time.time()
                delta = out_time - in_time
                res.encoding = 'utf-8'

                if addr in res.text:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}连接成功'.format(addr))
                    return self.write_html(addr, delta, type ,res)
                print(addr + '第' + str(i + 1) + "次连接失败,代理服务器响应内容错误")
            except (ReadTimeout, ConnectTimeoutError, ConnectTimeout) as e:
                print(str(proxies) + '第' + str(i + 1) + "次连接超时")
            except ProxyError:
                print(str(proxies), '代理出错')

    @staticmethod
    def write_html(addr, delta, type_,res):
        if not os.path.exists(api_settings.FILE_NAME):
            open(api_settings.FILE_NAME, 'w')
        with open(api_settings.FILE_NAME, 'r') as f:
            reader = csv.reader(f)
            for item in reader:
                if addr in item:
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}地址重复'.format(addr))
                    return
        with open(api_settings.FILE_NAME, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([addr, delta, type_,res.content.decode()])
            f.flush()
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}地址成功存储'.format(addr))

    def run(self):
        self.get_html()


if __name__ == "__main__":
    s01 = ProxiesSpider()
    s01.run()
