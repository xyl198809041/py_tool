import json
import time

from requests.cookies import cookiejar_from_dict

import pack.pyChrome as Chrome


class User:
    def __init__(self, UserName: str = '18806533976', PassWord='xyl88184668', JYWord='888612'):
        self.UserName = UserName
        self.PassWord = PassWord
        self.JYWord = JYWord


class ZheJin:

    def __init__(self, Buy_User: User, Data_User: User = User(), MinTianShu: int = 20, MinLiLv: float = 7.7,
                 MaxJinE: int = 5):
        self.web = Chrome.WebBrowser(False)
        self.Buy_web = Chrome.WebBrowser()
        self.MinTianShu = MinTianShu
        self.MinLiLv = MinLiLv / 100
        self.MaxJinE = MaxJinE * 10000
        self.Buy_User = Buy_User
        self.Data_User = Data_User

    def web_login(self):
        data = {
            "credential": self.Data_User.UserName,
            "password": self.Data_User.PassWord,
            "authCode": "",
            "returl": "",
            "encryptType": "1",
            "screenWidth": 1368,
            "screenHeight": 912,
            "host": "login.zjfae.com"
        }
        rt = self.web.PostJson('https://login.zjfae.com/ssm/ssm/pbonl.do?fh=VONLSSM000000J00', json.dumps(data))
        if rt['bd']['code'] != '0000':
            raise Exception('登录错误,错误:%s' % rt['bd']['desc'])
        self.web.BackWebBrowser.cookies = cookiejar_from_dict({'SMID': rt['bd']['smid']})
        self.Buy_web.Chrome.get('https://e.zjfae.com/front/login.html')
        # self.Buy_web.Chrome.find_element_by_css_selector('#username').send_keys(self.Buy_User.UserName)
        # self.Buy_web.Chrome.find_element_by_css_selector('#password').send_keys(self.Buy_User.PassWord)
        # self.Buy_web.Chrome.find_element_by_css_selector('#btnSubmit').click()
        # self.Buy_web.CheckUrl('https://e.zjfae.com/front/index.html')
        print('登录成功')

    def check_login(self):
        self.Buy_web.Chrome.get('https://e.zjfae.com/front/index.html')
        if self.Buy_web.CheckUrl('https://e.zjfae.com/front/login.html', 10):
            print('登录超时')
            self.Buy_web.Chrome.find_element_by_css_selector('#username').send_keys(self.Buy_User.UserName)
            self.Buy_web.Chrome.find_element_by_css_selector('#password').send_keys(self.Buy_User.PassWord)
            self.Buy_web.Chrome.find_element_by_css_selector('#btnSubmit').click()
            self.Buy_web.CheckUrl('https://e.zjfae.com/front/index.html')
            print('重新登录成功')
        else:
            print('登录依旧有效')

    def web_getlist(self):
        data = {
            'deadLineQuery': '',
            'expectedMaxAnnualRateQuery': '',
            'subjectTypeQuery': '',
            'buyerSmallestAmountQuery': '',  # 全
            # 'buyerSmallestAmountQuery': 1,  # 10w一下
            'availableAmountStartQuery': '',
            'availableAmountEndQuery': '',
            'orderBy': 'TARGET_RATE',
            'orderAsc': 1,
            'productName': '',
            'pageIndex': 1,
            'pageSize': 50
        }
        rt = self.web.PostJson('https://e.zjfae.com/ife/prdtransferquery/prdQueryTransferOrderListNew.html', data=data)
        if 'returnMsg' in rt:
            raise Exception(rt['returnMsg'])
        rt = rt['zjsWebResponse']
        if rt["returnCode"] == "0000":
            items = rt["data"]["productTradeInfoList"] if 'productTradeInfoList' in rt["data"] else []
            print('获取数量:%d' % len(items))
        else:
            raise Exception(rt["returnMsg"])
        for item in items:
            if int(item["leftDays"]) > self.MinTianShu and \
                    int(item["buyerSmallestAmount"]) <= self.MaxJinE and \
                    float(item["expectedMaxAnnualRate"]) >= float(self.MinLiLv):
                print(item)
                if int(item['delegateNum']) < int(item["buyerSmallestAmount"] * 2):
                    if self.MaxJinE >= int(item['delegateNum']):
                        item['buy_num'] = int(item['delegateNum'])
                        return item
                    else:
                        print('虽然符合,但是买的人太贱,多买了,最低:%dw,买了:%dw' % (
                            (int(item['buyerSmallestAmount']) / 10000), (int(item['delegateNum']) / 10000)))
                else:
                    if self.MaxJinE >= int(item["delegateNum"]):
                        item['buy_num'] = int(item['delegateNum'])
                        return item
                    else:
                        item['buy_num'] = self.MaxJinE
                        return item
        return None

    def web_buy(self, item):
        data = {
            "credential": self.Buy_User.UserName,
            "password": self.Buy_User.PassWord,
            "authCode": "",
            "returl": "",
            "encryptType": "1",
            "screenWidth": 1368,
            "screenHeight": 912,
            "host": "login.zjfae.com"
        }
        rt = self.Buy_web.PostJson('https://login.zjfae.com/ssm/ssm/pbonl.do?fh=VONLSSM000000J00', json.dumps(data))
        if rt['bd']['code'] != '0000':
            raise Exception('登录错误,错误:%s' % rt['bd']['desc'])
        # self.Buy_web.BackWebBrowser.cookies = cookiejar_from_dict({'SMID': rt['bd']['smid']})
        self.Buy_web.Chrome.add_cookie({'name': 'SMID', 'value': rt['bd']['smid']})
        self.Buy_web.Chrome.get('https://e.zjfae.com/front/product-zr-pay.html?productCode=&productName=&delegateNum'
                                '=%s&delegationCode=%s&quanDetailsId=' % (item["buy_num"], item['delegationCode']))
        self.Buy_web.Chrome.find_element_by_css_selector('#password').send_keys(self.Buy_User.JYWord)
        time.sleep(0.1)
        self.Buy_web.Chrome.find_element_by_css_selector('#btnPay').click()
        time.sleep(0.1)
        self.Buy_web.Chrome.find_element_by_css_selector('#btnPay').click()
