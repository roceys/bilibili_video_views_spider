import csv
import random
from multiprocessing import Process
import requests
from ip_pool.file_handler import CsvHelper


class Proxy:
    def __init__(self):
        self.url = 'http://httpbin.org/get'

    def examine_proxies(self):
        ip_list = Proxy._get_ip_list()
        print(ip_list)

        p_list = []
        for addr in ip_list:
            p = Process(target=self._do_exam, args=(addr,))
            p.daemon = True
            p_list.append(p)
            p.start()
        for p in p_list:
            p.join()

    def _do_exam(self, addr):
        proxies = {
            'http': 'http:' + addr,
            # 'http': 'http://61.157.206.174:37259',
            'https': 'https' + addr,
        }
        for i in range(5):
            try:
                res = requests.get(self.url, proxies=proxies, timeout=8)
                res.encoding = 'utf-8'
                # print(res.text)
                print(addr, '>>>>>>>>>>>', res.status_code)
                if "https://httpbin.org/get" not in res.text:
                    self._delete_addr(addr)
                break
            except Exception:
                print(addr, end='---->')
                print('failed for {}'.format(i), )
                if i == 4:
                    self._delete_addr(addr)
                    print('addr has failed for 4 times,do delete >>>>>>', addr)

    @staticmethod
    def get_proxy():
        ip_list = Proxy._get_ip_list()

        return random.choice(ip_list)

    @staticmethod
    def _get_ip_list():
        ip_list = []
        with open('proxies.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                ip_list.append(row[0])
        return ip_list

    def _delete_addr(self, addr):
        CsvHelper().delete_row(addr, 'proxies.csv')


if __name__ == '__main__':
    p01 = Proxy()
    # p01.get_proxy()
    p01.examine_proxies()
    # p01._delete_addr('aa')
