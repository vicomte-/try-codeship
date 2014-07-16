
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, Response

import requests
import lxml.html

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask! minimal R Version'

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

@app.route('/proxy_berlios')
def root():
    r = requests.get('http://' + hosttorequest + '/')
    headers = r.headers
##    headers['base'] = 'http://vicomte.pythonanywhere.com/proxy_berlios'
    resp = Response(r.content, status=r.status_code,
        mimetype=headers["content-type"])
    resp.headers.extend({'X-Powered-By': 'AT-5000'})
    resp.headers.extend(
        {'base': 'http://vicomte.pythonanywhere.com/proxy_berlios/'})
    print 'RESP HEADERS:', dict(resp.headers)
    return  resp

@app.route('/proxy_berlios/<path:other>')
def other(other):
    r = requests.get('http://' + hosttorequest + '/'+ other)
    return r.content

@app.route('/lxml_berlios')
def lxml_belios():
    page = requests.get('http://' + hosttorequest + '/')
    root = lxml.html.fromstring(page.text)
##    doc = lxml.html.parse('http://' + hosttorequest + '/')
##    root = doc.getroot()
    print 'LINKS BEFORE:', list(root.iterlinks())[-10:]
##    root.make_links_absolute('http://vicomte.pythonanywhere.com/lxml_berlios/', resolve_base_href=True)
    root.rewrite_links(replace_url, resolve_base_href=False)
    print 'LINKS AFTER:', list(root.iterlinks())[-10:]

##    return lxml.html.tostring(root, encoding=doc.docinfo.encoding)
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