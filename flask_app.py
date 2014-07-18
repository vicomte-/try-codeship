
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

import requests
import lxml.html
from init_this_service import initialize

app = Flask(__name__)
site_data = initialize()


@app.route('/')
def hello_world():
    return 'Hello from Flask! minimal R Version 2014-04-18#1 \n %s' % repr(site_data)

@app.route('/req')
def show_req():
    url = 'http://www.google.com'
    webcontent = requests.get(url)
    return 'success downloading %s' % url

@app.route('/berlios')
def show_berlios():
    url = 'http://www.berlios.de'
    webcontent = requests.get(url)
    print 'success downloading %s' % url
    return webcontent.content

hosttorequest = 'www.berlios.de'

@app.route('/proxy_berlios/<path:other>')
def other(other):
    r = requests.get('http://' + hosttorequest + '/'+ other)
    return r.content

@app.route('/lxml_berlios')
def lxml_belios():
    page = requests.get('http://' + hosttorequest + '/')
    root = lxml.html.fromstring(page.text)
    print 'LINKS BEFORE:', list(root.iterlinks())[-10:]
    root.rewrite_links(replace_url, resolve_base_href=False)
    print 'LINKS AFTER:', list(root.iterlinks())[-10:]
    return lxml.html.tostring(root, method='html',)

@app.route('/lxml_berlios/<path:other>')
def lxml_other(other):
    r = requests.get('http://' + hosttorequest + '/'+ other)
    return r.content

def replace_url(url):
    if url and url.startswith('/'):
        return '/lxml_berlios' + url
    else:
        return url