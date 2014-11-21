from datetime import datetime
from red import db
from helpers import is_it_text, convert_time_fromstring

class Websites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(40), unique=True)
    url = db.Column(db.String(120), unique=False)
    payload = db.Column(db.String(120), unique=False)
    created = db.Column(db.DateTime)

    def __init__(self, label = "", url = "", payload = "", created = ""):
        self.label = label
        self.url = url
        self.payload = payload
        if created:
            if is_it_text(created):
                self.created = convert_time_fromstring(created)
            else:
                self.created = created
        else:
            self.created = datetime.utcnow()

    def __repr__(self):
        return '<Website %r>' % self.label

    def __str__(self):
        return '%s|%s|%s' % (self.label, self.url, str(self.created))

    def make_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != 'id'}