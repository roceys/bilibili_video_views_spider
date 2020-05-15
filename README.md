# bilibili_video_views_spider
自动播放视频，配合换ip，cookie等可以刷一点点播放量

spider代理池是必要的 https://github.com/incinya/proxies
使用它可能要改下redis配置

# 爬坑日志
##提升selenium速度
driver.get()这个操作，改成不阻塞的

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
driver = webdriver.Chrome(executable_path='chromedriver.exe')

## 优化了browser_driver 结构
