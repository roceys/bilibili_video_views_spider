import requests
from selenium import webdriver
import api_settings
Options = webdriver.FirefoxOptions()

# 设置代理
Options.add_argument("--proxy-server=http://114.99.10.137:9999")
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Firefox(firefox_options=Options)

# 查看本机ip，查看代理是否起作用
browser.get(api_settings.URL_TEST)
print(browser.page_source)
input()
# 退出，清除浏览器缓存
browser.quit()


########################################

#
# proxies = {'https': '114.99.10.137:9999'}
#
# res = requests.get(
#     api_settings.URL_TEST,
#     timeout=10,
#     proxies=proxies)

end = 1
