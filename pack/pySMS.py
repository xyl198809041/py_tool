import json
import pack.pyChrome as pyChrome
import re
import datetime
import collections


class SMS:
    __loginurl = "http://svr51.huahai.net/SSL.svc/Login?DevVer=8.0.0&OS=2&Username=%s&ClientVer=5.1&Orgcode=05660&Password=%s"
    __sendurl = "http://svr51.huahai.net/UploadService/SubmitSMS"
    __user = {"loginPhone": "xuyl", "password": "xyl88184668"}
    __token = ""

    def __init__(self, default_phonenum: str = None):
        self.Web = pyChrome.WebBrowser(False)
        self.IsLogin = False
        if default_phonenum != None:
            self.default_phonenum = default_phonenum

    def Login(self):
        json = self.Web.GetJson(self.__loginurl % (self.__user["loginPhone"], self.__user["password"]))
        if json["Code"] == "0":
            self.IsLogin = True
            self.__token = json["Data"]["Token"]

    def SendSMS(self, phonenum: str = None, msg: str = None):
        if not self.IsLogin:
            self.Login()
        if phonenum is None:
            if self.default_phonenum is None:
                print("错误:号码缺失")
                return
            else:
                phonenum = self.default_phonenum
        data1 = collections.OrderedDict()
        data1['token'] = self.__token
        data1['recObject'] = '0566021' + phonenum
        data1['content'] = msg
        data1['sendTime'] = 0
        data1['recState'] = 0
        data1['msgType'] = 1
        data1['batchNumber'] = int(datetime.datetime.now().timestamp())
        data1['os'] = 2
        data1['reqCount'] = 1

        j = self.Web.PostJson(self.__sendurl, data=data1)
        if j["Code"] == "0":
            print("向%s发送短信成功" % phonenum)
        else:
            self.IsLogin = False
            print("发送短信失败")
            print(j)


def SendSMS(phonenum: str, msg: str):
    SMS().SendSMS(phonenum, msg)
