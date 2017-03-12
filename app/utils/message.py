import re
import urllib
import requests
from lxml import html

# 登录的主页面
HOST = 'http://10.72.66.180'
LOGIN = '/rone/login'
ADD_MESSAGE = '/affairs/affSMSApply/addNotice'
SEND_MASSAGE = '/affairs/affSMSApply/saveNotice'



class ParamsJson(object):
    applyDeptCode = ''
    applyDeptName = ''
    applyUserName = ''
    applyUserCode = ''
    topOrgCode = ''
    smsContent = ''

    def get_params(self, page):
        # print(page.text)
        tree = html.fromstring(page.text)
        parsed_tree = tree.xpath('//*[@id="divSelGroup"]/table/tr/td/input')

        # 短信页面拿以下的参数
        self.applyDeptCode = parsed_tree[0].value
        self.applyDeptName = parsed_tree[1].value
        self.applyUserName = parsed_tree[2].value
        self.applyUserCode = parsed_tree[3].value
        self.topOrgCode = parsed_tree[5].value


class ContactJson(object):
    def __init__(self):
        self.receiveUserCode = ''
        self.receiveUserName = ''
        self.receiveUserPhone = ''
        self.smsScheduler = ''
        self.sendMessageValue = '0'


class AddNoticeParams(object):
    def __init__(self):
        self.result = 'login'
        self.menuType = 3
        self.mgId = 37
        self.menuId = 121
        self.resuuid = '8ac89d6039dc2e600139dc2f39cc0001'
        self.LTPAToken = ''
        self.appId = '8ac8c23239d246830139d3f531770008'


class LoginWorker(object):
    def __init__(self):
        self.userid = ''
        self.userName = ''
        self.j_username = ''
        self.password = ''
        self.j_password = ''

    def login(self, session, username, password):
        self.userid = username
        self.userName = username
        self.j_username = username
        self.password = password
        self.j_password = password

        page = session.post(HOST + LOGIN, data=self.__dict__)
        print(page.text)
        print(page.status_code)
        m = re.search(r'LTPAToken=(.*)"', page.text)
        return m.group(1)


class SendMessageWorker(object):
    def __init__(self, username, password):
        self.params_json = ParamsJson()
        self.contact_json = ContactJson()
        self.add_notice_params = AddNoticeParams()
        self.login_params = LoginWorker()
        self.session = requests.Session()

        # 从首页取得LTPAToken
        token = self.login_params.login(session=self.session, username=username, password=password)
        self.add_notice_params.LTPAToken = token

        # 从短信页面取得发短信的所需字段
        page = self.session.get(HOST + ADD_MESSAGE, params=self.add_notice_params.__dict__)
        self.params_json.get_params(page)


    def send_message(self, sms_content, receiver_phone):
        self.params_json.smsContent = sms_content
        self.contact_json.receiveUserPhone = receiver_phone
        data = dict(
            paramsJson=self.params_json.__dict__,
            contactJson=self.contact_json.__dict__
        )
        data = urllib.parse.urlencode(data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        self.session.post(HOST+SEND_MASSAGE, data=data, headers=headers)


if __name__ == "__main__":
    worker = SendMessageWorker('liaozqhh1', 'yx123456lzq')
    # worker.send_message('hello world', '15607444616')
