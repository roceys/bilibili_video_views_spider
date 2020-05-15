# bilibili_video_views_spider
自动播放视频，配合换ip，cookie等可以刷一点点播放量

一个代理池 https://github.com/incinya/proxies

# 爬坑日志
提升selenium速度
driver.get()这个操作，改成不阻塞的

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(executable_path='chromedriver.exe')


