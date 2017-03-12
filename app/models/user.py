

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

