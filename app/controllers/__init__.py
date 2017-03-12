from flask import render_template
from flask import session
from flask import Blueprint

from ..models import User


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


@main.route('/timeline/<username>')
def user_timeline_view(username):
    u = User.query.filter_by(username=username).first_or_404()
    return render_template('timeline.html', user=u)
