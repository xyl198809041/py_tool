from selenium.webdriver.chrome.webdriver import WebDriver
from requests import Session
from requests.cookies import cookiejar_from_dict
import requests
import time
import json
import urllib3
import requests.adapters
import html
import pyquery
from pack.threadByQueue import threadByQueue
import re


class WebBrowser:

    def __init__(self, IsUserChrome: bool = True, IsProxy: bool = False, timeout: int = 1):
        self.timeout = timeout
        if IsUserChrome: self.Chrome = WebDriver()
        self.IsProxy = IsProxy
        self.ProxyIpList = list()
        self.ResetBackWebBrowser()
        urllib3.disable_warnings()
        if IsProxy:
            self.proxy_thread = threadByQueue(10, target=self.check_proxy, args=self.GetWebProxyIpList())
            self.proxy_thread.start()

    def ResetBackWebBrowser(self):
        self.BackWebBrowser = Session()
        self.BackWebBrowser.keep_alive = False
        self.BackWebBrowser.verify = False
        self.BackWebBrowser.headers[
            'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
        self.BackWebBrowser.headers['Accept-Language'] = 'zh-Hans-CN,zh-Hans;q=0.5'
        self.BackWebBrowser.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        self.BackWebBrowser.headers['Connection'] = 'close'
        self.IsLogin = False

    def GetWebProxyIpList(self):
        # 第一种
        return [p('td').eq(1).text() + ':' + p('td').eq(2).text() for p in
                pyquery.PyQuery(self.BackWebBrowser.get('http://www.xicidaili.com/nn/').text)(
                    '#ip_list>tr').items()][1:]
        # #第二种
        # html=self.BackWebBrowser.get('http://www.89ip.cn/tqdl.html?api=1&num=30&port=&address=&isp=').text
        # return re.findall(r'''\d+\.\d+.\d+\.\d+:\d+''',html )
        # #第三种
        # return re.findall(r'''\d+\.\d+.\d+\.\d+:\d+''',requests.get('http://www.66ip.cn/nmtq.php?api=66ip').text)

    def GetProxyIp(self, IsNew: bool = False) -> str:
        while len(self.ProxyIpList) <= 3:
            print('代理服务器测试中.....')
            print(self.ProxyIpList)
            time.sleep(10)
        if len(self.ProxyIpList) < 10 and len(self.proxy_thread.args) < 20:
            self.proxy_thread.args.extend(self.GetWebProxyIpList())
        if IsNew:
            self.ProxyIpList.pop(0)
            print('代理服务器列表还剩' + str(len(self.ProxyIpList)) + '个')
            return self.ProxyIpList[0]
        else:
            return self.ProxyIpList[0]

    def check_proxy(self, ip: str):
        for i in range(5):
            try:
                time.sleep(1)
                ipconfig = requests.get('http://pv.sohu.com/cityjson?ie=utf-8',
                                        timeout=self.timeout,
                                        proxies={'https': ip,
                                                 'http': ip
                                                 },
                                        headers={'Connection': 'close'}).text
                if ipconfig.find(ip.split(':')[0]) != -1 or ipconfig.find('returnCitySN') != -1:
                    self.ProxyIpList.append(ip)
                    print(ip + '\n' + ipconfig + '\n代理服务器测试成功')
                    return
                else:
                    pass
                    # print(ip + '第' + str(i) + '次测试失败重试,信息:' + ipconfig)
            except Exception as e:
                pass
                # print(ip + '第' + str(i) + '次测试失败重试,信息:' + str(e))
        # print(ip + '测试失败')

    # def ProxyTest(self, Next: bool = False):
    #     if Next:
    #         self.GetProxyIp(True)
    #     while True:
    #         try:
    #             ipconfig = self.BackWebBrowser.get('http://pv.sohu.com/cityjson?ie=utf-8',
    #                                                timeout=self.timeout,
    #                                                proxies={'https': self.GetProxyIp(),
    #                                                         'http': self.GetProxyIp()
    #                                                         }).text
    #             if ipconfig.find(self.GetProxyIp().split(':')[0]) != -1:
    #                 print(ipconfig + '\n代理服务器连接成功')
    #                 self.ResetBackWebBrowser()
    #                 break
    #             else:
    #                 print('测试失败返回信息:' + ipconfig)
    #                 print('测试代理服务器:' + self.GetProxyIp(True))
    #         except Exception as e:
    #             print(e)
    #             print('测试代理服务器:' + self.GetProxyIp(True))

    def Login(self, login_url: str, check_url: str):
        self.Chrome.get(login_url)
        self.CheckUrl(check_url)
        self.Sync_cookie()
        print("登录完成")

    def Sync_cookie(self):
        cookie = self.Chrome.get_cookies()
        requests_cookie = {}
        for c in cookie:
            requests_cookie[c["name"]] = c["value"]
        self.BackWebBrowser.cookies = cookiejar_from_dict(requests_cookie)

    def Set_cookid(self, cookie):
        requests_cookie = {}
        for c in cookie:
            requests_cookie[c["name"]] = c["value"]
        self.BackWebBrowser.cookies = cookiejar_from_dict(requests_cookie)

    def GetHtml(self, url: str, encoding: str = "utf8"):
        i = 0
        while True:
            try:
                if self.IsProxy:
                    return self.BackWebBrowser.get(url, timeout=self.timeout,
                                                   proxies={'https': self.GetProxyIp(),
                                                            'http': self.GetProxyIp()
                                                            }).content.decode(encoding)
                else:
                    return self.BackWebBrowser.get(url, timeout=self.timeout).content.decode(encoding)
            except Exception as e:
                i = i + 1
                print("连接错误" + url)
                print(e)
                if self.IsProxy and i % 5 == 0:
                    self.GetProxyIp(True)

    def GetHtmlByPyQuery(self, url: str, encoding: str = 'utf8'):
        return pyquery.PyQuery(self.GetHtml(url, encoding))

    def GetJson(self, url: str, encoding: str = "utf8"):
        html = self.GetHtml(url, encoding)
        obj = json.loads(html)
        return obj

    def PostHtml(self, url: str, data, encoding: str = "utf-8"):
        while True:
            # try:
            return self.BackWebBrowser.post(url, data=data, timeout=self.timeout).content.decode(encoding)
        # except Exception as e:
        #     print("连接错误" + url)
        #     print(e)

    def PostJson(self, url: str, data, encoding: str = "utf-8"):
        while True:
            # try:
            html = self.PostHtml(url, data, encoding)
            obj = json.loads(html)
            return obj
        # except:
        #     print("连接错误" + url)

    def CheckUrl(self, CheckUrl, wait_time: int = 60) -> bool:
        while wait_time > 0:
            if self.Chrome.current_url.find(CheckUrl) != -1:
                break
            time.sleep(1)
            wait_time = wait_time - 1
        time.sleep(1)
        return wait_time > 0
