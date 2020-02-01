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
# ONE_VIDEO_ADDR = 'https://www.bilibili.com/video/av20379071/'
ONE_VIDEO_ADDR = 'https://www.bilibili.com/video/av25107072/'
ACT_PROXY = False
PLAY_ONE_VIDEO = False
WAIT_TIME = 20
PLAY_DURATION = 30
ACT_HEADLESS = False
PRINT_LOG = True
MAX_THREAD = 1
ACT_PROCESS = True

