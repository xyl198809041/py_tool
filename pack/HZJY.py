import pack.pyChrome as chrome
import threading
import json

_hzjy = None


def hzgy():
    """
使用杭州教育
    :return:
    """
    global _hzjy
    if _hzjy is None:
        _hzjy = HZJY()
    return _hzjy


class HZJY:

    def __init__(self, uuid='123457', userid='923071', sign='396116cde5e191f59aacf9a4a066338d'):
        self.__is_login = False
        self.__resend_num = 0
        self.__web = chrome.WebBrowser(False)
        self.__uuid = uuid
        self.__userid = userid
        self.__sign = sign
        self.__login_data = None

    def __login(self):
        self.__web = chrome.WebBrowser(False)
        self.__web.BackWebBrowser.get('http://app.hzedu.gov.cn/api/barq?uuid=%s' % self.__uuid)
        self.__web.GetHtml('https://app.hzedu.gov.cn/api/login?sign=%s&uuid=%s&userid=%s' %
                           (self.__sign, self.__uuid, self.__userid))
        self.__login_data = self.__web.GetJson('http://app.hzedu.gov.cn/api/asklogin?uuid=%s' % self.__uuid)
        token = self.__login_data['data']['context']['token']['token']
        self.__web.BackWebBrowser.headers['x-access-token'] = token
        self.__is_login = True
        print('登录成功')

    def get_students(self):
        data = self.__web.PostJson('http://app.hzedu.gov.cn/api/api', '{act: "getOrgTree", orgid: %s, peopleid: %s}' %
                                   (self.__login_data['data']['context']['schools'][0]['orgstructid'],
                                    self.__login_data['data']['context']['currentuser']['peopleid']))
        students = self.__web.PostJson('http://app.hzedu.gov.cn/api/api',
                                       '{act: "getStudentByOrgid", orgid: %s, pageindex: 0, pagesize: 100, positionid: 5}' %
                                       data['data']['childs'][0]['childs'][0]['orgid'])
        print(students)

    def send_msg(self, title: str = '题目', msg: str = '内容', senderInfo: str = '', to_id: str = '424736:923071'):
        """
        发送信息
        :param title: 标题
        :param msg: 内容
        :param senderInfo: 发送者落款
        :param to_id: 对象,格式:peopleid:userid
        """
        # return
        def f():
            if not self.__is_login:
                self.__login()
            data = '''{"act":"addNotice","orgid":%s,"senderid":%s,"status":2,"sendTime":"","notice":{"senderInfo":"%s", 
            "title":"%s","content":"%s","logo":"","isEncrypt":0,"isImportant":0,"isMessage":0,"isTimer":0,"sendRange":"", 
            "notifynum":0},"attachstr":[],"receiverstr":{"orgids":"","peoples":"[{\\"peopleid\\":%s,\\"userid\\":%s,
            \\"isStudent\\":0}]"}}''' % \
                   (self.__login_data['data']['context']['schools'][0]['orgstructid'],
                    self.__login_data['data']['context']['currentuser']['peopleid'],
                    senderInfo,
                    title,
                    msg,
                    to_id.split(':')[0],
                    to_id.split(':')[1])
            try:
                self.__web.PostJson('http://app.hzedu.gov.cn/api/api', data=data.encode('utf-8'))
                self.__resend_num = 0
            except Exception as e:
                print(e)
                self.__is_login = False
                if self.__resend_num < 3:
                    self.__resend_num = self.__resend_num + 1
                    self.send_msg(title=title, msg=msg, senderInfo=senderInfo, to_id=to_id)
                else:
                    print('发送失败')
        # threading.Thread(target=f).run()
