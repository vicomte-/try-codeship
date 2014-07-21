# A very simple Flask Hello World app for you to get started with...

from flask import Flask

import requests
import lxml.html
from init_this_service import initialize
from urlparse import urlsplit

app = Flask(__name__)
site_data = initialize()


@app.route('/')
def hello_world():
    return 'Hello from Flask! minimal R Version 2014-07-21#6 \n %s' % repr(site_data)

@app.route('/req')
def show_req():
    url = 'http://www.google.com'
    webcontent = requests.get(url)
    return 'success downloading %s' % url

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
