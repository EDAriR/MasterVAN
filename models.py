from app import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


class User(db.Model):
    __tablename__ = 'users'

    sequence = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(10))
    name = db.Column(db.String(255))
    birthday = db.Column(db.DateTime)
    phone = db.Column(db.String(10))
    email = db.Column(db.String(255))
    google = db.Column(db.String(255))
    facebook = db.Column(db.String(255))
    line = db.Column(db.String(255))

    def __init__(self, id, name, birthday, phone, email, google, facebook, line):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.phone = phone
        self.email = email
        self.google = google
        self.facebook = facebook
        self.line = line

    def __repr__(self):
        return '<id: {}>'.format(self.id) + '<, name: {}>'.format(self.name) + '<, email: {}>'.format(self.email)