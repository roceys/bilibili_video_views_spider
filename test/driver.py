import os
import requests
from selenium import webdriver
from spider.proxy_model import ProxyStack

os.chdir('../')
ops = webdriver.ChromeOptions()
proxy_pool = ProxyStack()
proxy = proxy_pool.get_random()
print(proxy)
# ops.add_argument('--headless')
# ops.add_argument('--disable-dev-shm-usage')
# ops.add_argument('--disable-gpu')
# ops.add_argument('--user-agent=%s' % ua)
# ops.add_argument('--no-sandbox')
ops.add_argument('--proxy-server=http://%s' % proxy)
driver = webdriver.Chrome(chrome_options=ops)
driver.get("http://httpbin.org/get")
proxys = {'http': proxy, 'https': proxy}
res = requests.get("http://httpbin.org/get", proxies=proxys)
# origin 182.150.187.244
print(res.text)
input()
