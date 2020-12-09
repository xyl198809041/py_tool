import pack.pyChrome as chrome

web = chrome.WebBrowser(proxy='127.0.0.1:8888')
web.Chrome.get('http://www.baidu.com')
