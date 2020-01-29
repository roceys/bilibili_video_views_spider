FILE_NAME = __file__.replace('api_settings.py', 'proxies.csv')
TIME_OUT = 2
URL_MAIN = 'https://www.xicidaili.com/nn/{}.html'
URL_TEST = 'http://httpbin.org/get'
XIGUA_URL = 'http://api3.xiguadaili.com/ip/?tid=556221803609687&num=40'
XG_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'api3.xiguadaili.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
}
USE_PROXY_TO_XICI = False
THREAD_DELTA = 1
