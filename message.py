import requests
import json
import http
import urllib

# 登录的主页面
HOSTURL = 'http://10.72.66.180'
# post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
LOGINURL = 'http://10.72.66.180/rone/login'

SEND_MASSAGE_API = "http://10.72.66.180/affairs/affSMSApply/saveNotice"
USER_ID = 'liaozqhh'
PASSWORD = 'yx123456lzq'


# TODO 接口细化，从网页抓取用户信息填入data
def gen_post_data():
    paramsJson = {
        "applyDeptCode": "01243120306",
        "applyDeptName": "市场服务分部",
        "applyUserName": "廖志强",
        "applyUserCode": "4214312011793",
        "topOrgCode": "012431203",
        "smsContent": "接口问题搞定！",
    }

    contactJson = {
        "receiveUserCode": "",
        "receiveUserName": "",
        "receiveUserPhone": "15607444616",
        "smsScheduler": "",
        "sendMessageValue": "0"
    }

    data = dict(
        paramsJson=paramsJson,
        contactJson=contactJson
    )

    return urllib.parse.urlencode(data)


def send_message(session):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    postData = gen_post_data()
    r = session.post(SEND_MASSAGE_API, data=postData, headers=headers)
    print(r.content.decode())


def login(username, password):
    username = 'liaozqhh'
    password = 'yx123456lzq'
    data = dict(
        userid=username,
        userName=username,
        j_username=username,
        password=password,
        j_password=password,
    )

    login_url = 'http://10.72.66.180/rone/login'
    sss = requests.Session()
    sss.post(login_url, data=data)

    return sss


if __name__ == "__main__":
    session = login(username=USER_ID, password=PASSWORD)
    send_message(session)


