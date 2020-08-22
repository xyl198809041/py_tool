from selenium.webdriver.remote.webelement import WebElement

import pack.pyChrome
import asyncio

web=pack.pyChrome.WebBrowser(is_load_img=False)
web.Chrome.get('http://www.baidu.com')
a=web.Get_cookie_str()
print(a)