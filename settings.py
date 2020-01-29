SPACE_ID = '10241912'
MY_URL = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp'.format(
    SPACE_ID, '{}')
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'api.bilibili.com',
    'Origin': 'https://space.bilibili.com',
    'Pragma': 'no-cache',
    'Referer': 'https://space.bilibili.com/10241912/video',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
ONE_VIDEO_ADDR = 'https://www.bilibili.com/video/av20379071/'
PLAY_ONE_VIDEO = True
SLEEP_TIME = 5
ACT_HEADLESS = False
PRINT_LOG = True
MAX_THREAD = 2
ACT_PROCESS = True

