# bilibili_video_views_spider
刷b站播放数的“爬虫”

b站一个ip每天只能刷一次播放量，所以还需要维护一个ip池
参考这个小项目https://github.com/incinya/proxies

提升selenium速度的小技巧
driver.get()这个操作，改成不阻塞的就行了，这样打开网页就操作完成了，不需要等他加载
下面我可以直接等待需要的元素出现即可进行操作
配置也是很简单


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(executable_path='chromedriver.exe')
复制代码
配置一个参数，就是页面加载策略，系统默认是等待，就是等他加载完，直接设置成none，就是不等待，这样就是get操作完后直接就是结束了

不影响下面的操作，这样就可以愉快的玩耍了

