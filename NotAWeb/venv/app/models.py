from app import db

class User(db.Model):
    id = db.Column(db.Integer, primery_key=True)
    login = db.Column(db.String(64), index=True,unique=True)
    password = db.Column(db.String(128), index=True,unique=True)
    def __repr__(self):
        return '<User %r>' %(self.login)
