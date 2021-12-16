import pack.pyChrome as chrome

web = chrome.WebBrowser(False)
web.BackWebBrowser.headers['Content-Type'] = 'application/x-www-form-urlencoded'
rt = web.PostJson('https://daydayup.96225.com/hcswipeback/login', data='username=gsq_admin_0091&password=149ee0e92e03ae4b84b32ef992ba3921')
print(rt)
