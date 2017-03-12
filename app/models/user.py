

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    # 外键关联

    @staticmethod
    def user_by_name(username):
        return User.query.filter_by(username=username).first()


    def save(self):
        db.session.add(self)
        db.session.commit()

