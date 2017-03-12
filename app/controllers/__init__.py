import csv
import io

from flask import render_template
from flask import session
from flask import Blueprint
from flask import request
from flask import jsonify

from ..models import User
from ..utils.message import SendMessageWorker


main = Blueprint('controllers', __name__)


# 通过 session 来获取当前登录的用户
def current_user():
    # print('session, debug', session.permanent)
    username = session.get('username', '')
    u = User.query.filter_by(username=username).first()
    return u


@main.route('/timeline')
def timeline_view():
    u = current_user()
    return render_template('timeline.html', user=u)


@main.route('/upload', methods=['POST'])
def upload_file():
    print('upload')
    u = current_user()
    s = SendMessageWorker(username=u.username, password=u.password)
    # 通过 request.files 访问上传的文件
    # uploaded 是上传时候的文件名
    file = request.files.get('uploaded')
    if not file:
        return '<h1>没有上传</h1>'


    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)

    for row in csv_input:
        s.send_message(row[0], row[1])

    # TODO 返回短信的状态
    r = {
        'success': True,
        'message': '发送完成',
    }
    return jsonify(r)

