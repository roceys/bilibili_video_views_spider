from selenium import webdriver
from selenium.webdriver.chrome.options import Options

proxy = '117.90.4.159:9999'
ops = Options()
# ops.add_argument('--headless')
# ops.add_argument('--disable-dev-shm-usage')
# ops.add_argument('--disable-gpu')
# ops.add_argument('--user-agent=%s' % ua)
ops.add_argument('--no-sandbox')
ops.add_argument('--proxy-server=http://%s' % proxy)
driver = webdriver.Chrome(chrome_options=ops)
driver.delete_all_cookies()


print('--proxy-server=http://%s' % proxy)
driver.get("http://httpbin.org/get")


