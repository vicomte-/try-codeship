# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import requests
import lxml.html
from init_this_service import initialize
from urlparse import urlsplit

from datetime import datetime
app = Flask(__name__)

db_pwd, site_data = initialize()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://vicomte:%s@mysql.server/vicomte$default' % db_pwd

db = SQLAlchemy(app)

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


## from db_model import Websites

@app.route('/')
def hello_world():
    return 'Hello from Flask! minimal R Version 2014-07-21#6 \n %s' % repr(site_data)

@app.route('/sites')
def show_sites():
    sites = Websites.query.all()
    return 'sites configured: %s' % '\n<p>'.join(map(str, sites))

@app.route('/sites/add/<string:data>')
def add_sites(data):
    label, url = data.split(',')
    newsite = Websites(label, url)
    db.session.add(newsite)
    db.session.commit()

    return 'site added: %s' % newsite

@app.route('/redirect/<string:domain>')
def show_redirect(domain):

    def replace_url(url):
        if url:
            url_parts = urlsplit(url)
            if url.startswith('/'):
                return '/redirect/' + domain + url
            elif not url_parts.scheme:
                return '/redirect/' + domain +'/' + url
            else:
                return url

    try:
        page = requests.get('http://' + site_data[domain] + '/')
    except KeyError:
        return 'No url found for symbol "%s", check ini file.' % domain
    root = lxml.html.fromstring(page.text)
##    print 'LINKS BEFORE:', list(root.iterlinks())[-10:]
    root.rewrite_links(replace_url, resolve_base_href=False)
##    print 'LINKS AFTER:', list(root.iterlinks())[-10:]
    return lxml.html.tostring(root, method='html',)

@app.route('/redirect/<string:domain>/<path:other>')
def redirect_other(domain, other):
    r = requests.get('http://' + site_data[domain] + '/'+ other)
    return r.content