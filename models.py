from datetime import datetime
from flask_app import db

__author__ = 'Surfer'


class Websites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(40), unique=True)
    url = db.Column(db.String(120), unique=False)
    created = db.Column(db.DateTime)

    def __init__(self, label, url):
        self.label = label
        self.url = url
        self.created = datetime.utcnow()

    def __repr__(self):
        return '<Website %r>' % self.label

    def __str__(self):
        return '%s|%s|%s' % (self.label, self.url, str(self.created))


