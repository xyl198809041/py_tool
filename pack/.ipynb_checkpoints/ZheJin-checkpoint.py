import pack.pyChrome as pyChrome
import json


class ZheJin:
    UserName = "18806533976"
    PassWord = "MTQ4OGZhZDE5OGU3MTkwODM3MzRlMDEzYmMwZTU5ZTQ="
    JYPW = "ZWJkMmE5MDI4MTM0ODllN2ZmMDY2MjE2N2MyNGUyMzE=1"
    Web = pyChrome.WebBrowser(False)
    LoginUrl = "https://me.zjfae.com/ife/azj/pbaft.do?fh=VAFTAZJ000000J00&p=and&pbname=PBAPP_login&registrationId" \
               "=100d855909770e4c2b9&clientOsver=8&platform=android&appVersion=2.1.6.48&deviceModal=DUK-AL20&deviceNo" \
               "=48a5fa0ca78a0981&userid=13067764287&ReqTime=1518173832200 "
    ListUrl = "https://me.zjfae.com/ife/mzj/pbife.do?fh=VREGMZJ000000J00&p=and&pbname" \
              "=PBIFE_prdtransferquery_prdQueryTransferOrderListNew&clientOsver=8&platform=android&appVersion=1.6.43" \
              "&deviceModal=DUK-AL20&deviceNo=48a5fa0ca78a0981&userid=13067764287&ReqTime=1518174934516 "
    LiuShuiUrl = "https://me.zjfae.com/ife/mzj/pbife.do?fh=VREGMZJ000000J00&p=and&pbname=PBIFE_trade_queryPayInit" \
                 "&clientOsver=8&platform=android&appVersion=2.1.6.48&deviceModal=DUK-AL20&deviceNo=48a5fa0ca78a0981" \
                 "&userid=13067764287&ReqTime=1518175628498 "
    BuyUrl = 'https://me.zjfae.com/ife/mzj/pbife.do?fh=VREGMZJ000000J00&p=and&pbname=PBIFE_trade_transferOrder' \
             '&clientOsver=8&platform=android&appVersion=2.1.6.48&deviceModal=DUK-AL20&deviceNo=48a5fa0ca78a0981&userid' \
             '=13067764287&ReqTime=1518175646587 '

    @classmethod
    def login(cls):
        cls.Web.timeout = 10
        data = {
            "username": cls.UserName,
            "password": cls.PassWord,
            "loginMethod": "0",
            "needValidateAuthCode": "0",
            "authCode": "0",
            "isOpenGpwd": "0"
        }
        cls.Web.BackWebBrowser.headers.setdefault("Content-Type", "application/json;charset=UTF-8")
        rt = cls.Web.PostJson(cls.LoginUrl, json.dumps(data))
        if rt["body"]["returnCode"] == "0000":
            return True
        else:
            raise Exception(rt["body"]["returnMsg"])

    @classmethod
    def loadlist(cls):
        
        data = {
            "pageIndex": "1",
            "pageSize": "50",
            "uuids": "",
            #5-20w
            "uuids": "1006-2016-",
            "productName": ""
        }
        rt = cls.Web.PostJson(cls.ListUrl, json.dumps(data))
        if rt["body"]["returnCode"] == "0000":
            return rt["body"]["data"]["productTradeInfoList"]
        else:
            raise Exception(rt["body"]["returnMsg"])

    @classmethod
    def liushui(cls, data, JinE: int):
        data = {
            "productCode": data["delegationCode"],
            "delegateNum": JinE * 10000,
            "payType": "transferPay",
            "orderType": ""
        }
        rt = cls.Web.PostJson(cls.LiuShuiUrl, json.dumps(data))
        if rt["body"]["returnCode"] == "0000":
            return rt["body"]["data"]["payInitWrap"]["repeatCommitCheckCode"]
        else:
            raise Exception(rt["body"]["returnMsg"])

    @classmethod
    def buy(cls, data, JinE: int, LiuShui: str):
        data = {
            "delegationCode": data["delegationCode"],
            "buyNum": JinE,
            "repeatCommitCheckCode": LiuShui,
            "payType": "1",
            "password": cls.JYPW,
            "channelNo": "12",
            "kqCode": "",
            "kqType": "",
            "kqValue": ""
        }
        print(data)
        rt = cls.Web.PostJson(cls.BuyUrl, json.dumps(data))
        if rt["body"]["returnCode"] == "0000":
            return True
        else:
            raise Exception(rt["body"]["returnMsg"])


