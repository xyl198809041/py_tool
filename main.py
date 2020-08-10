from selenium.webdriver.remote.webelement import WebElement

import pack.pyChrome
import asyncio

web=pack.pyChrome.WebBrowser(is_load_img=False)
web.Chrome.get('''http://www.8t88.com/html/88/7187.htm''')

a:WebElement=asyncio.run(web.asyncFindElement_by_css_selector('body > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(4) > a'))
a.click()
input()