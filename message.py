import requests
import json
import http
import urllib
from time import sleep

SEND_MASSAGE_API = "http://10.72.66.180/affairs/affSMSApply/saveNotice"
USER_ID = 'liaozqhh'
PASSWORD = 'yx123456lzq'


def gen_post_data():
    # url = api
    applyMessage = {"applyDeptCode": "01243120306", "applyDeptName": "市场服务分部", "applyUserName": "廖志强",
                    "applyUserCode": "4214312011793", "applyUserPhone": "", "topOrgCode": "012431203",
                    "smsContent": "接口问题搞定！", "isGroupSend": "0", "smsType": "NOTICE", "isReply": 0}
    applyMessageJsonStr = json.dumps(applyMessage)

    contactMessage = {"receiveUserCode": "", "receiveUserName": "廖志强", "receiveUserPhone": "15607444616",
                      "smsScheduler": "", "sendMessageValue": "0"}
    contactMessageJsonStr = json.dumps(contactMessage)

    message = "paramsJson=" + urllib.parse.quote(applyMessageJsonStr) + "&contactJson=" + urllib.parse.quote(
        contactMessageJsonStr)
    # r = requests.post(url,json=message)
    return message

# 登录的主页面
hosturl = 'http://10.72.66.180'
# post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
posturl = 'http://10.72.66.180/rone/login'


def login(username=USER_ID, password=PASSWORD):
    # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

    # 打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
    h = urllib.request.urlopen(hosturl)

    # 构造Post数据，他也是从抓包里分析得出的。
    postData = {'userid': username,
                'linkpage': '',
                'userName': username,
                'j_username': username,
                'password': password,
                'j_password': password,
                'logoutExitPage': 'SignOnServlet',
                }

    # 需要给Post数据编码
    postData = urllib.parse.urlencode(postData).encode('utf-8')

    # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
    request = urllib.request.Request(posturl, postData)
    print(request)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    print(text)


def send_message():
    # 构造Post数据，他也是从抓大的包里分析得出的。
    postData = gen_post_data().encode('utf-8')

    # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
    request = urllib.request.Request(SEND_MASSAGE_API, postData)
    print(request)
    response = urllib.request.urlopen(request)
    text = response.read().decode('utf-8')
    print(text)
    # sleep(5)
    # TODO 尝试用多线程解决延迟问题


if __name__ == "__main__":
    login()
    for i in range(3):
        send_message()

        # TODO 接口细化，从网页抓取用户信息填入data
