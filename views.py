import os
import lxml.html
import requests
from urllib import unquote_plus
from urlparse import urlsplit
from flask import request, session, flash, url_for, render_template, redirect
from functools import wraps
from helpers import check_logged_in, mark_as_preformatted, calc_expiration
from helpers import set_default
from flask_app import app, db, site_data
from models import Websites

__author__ = 'Surfer'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_logged_in():
            return login()
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def default():
    return 'Hello from Flask! minimal R Version 2014-07-21#6 \n %s' % repr(site_data)


@app.route('/sites')
@requires_auth
def show_sites():
    sites = Websites.query.all()
    return 'sites configured: \n%s' % mark_as_preformatted(
        '\n'.join(map(str, sites)))


@app.route('/sites/add/<string:data>')
@requires_auth
def add_sites(data):
    label, url = map(unquote_plus, data.split(','))
    newsite = Websites(label, url)
    db.session.add(newsite)
    db.session.commit()

    return 'site added: %s' % newsite


@app.route('/dbcreate')
@requires_auth
def dbcreate():
    db.create_all()
    return 'database created'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != set_default(
                os.environ.get('USER'), 'user'):
            error = 'Invalid username'
        elif request.form['password'] != set_default(
                os.environ.get('PASSWORD'), 'pwd'):
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['expiration'] = calc_expiration()
            flash('You were logged in')
            return redirect(url_for('default'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('default'))


@app.route('/env')
@requires_auth
def show_env():
    env_settings = sorted(os.environ.items())
    html = '\n'.join(('%s = %s' % (k, v) for k, v in env_settings))
    return mark_as_preformatted(html)


@app.route('/env/add/<string:data>')
@requires_auth
def add_env(data):
    k, v = data.split(',')
    os.environ[k] = v
    return 'env added: %s=%s' % (k, v)


@app.route('/redirect/<string:domain>')
def show_redirect(domain):
    def replace_url(url):
        if url:
            url_parts = urlsplit(url)
            if url.startswith('/'):
                return '/redirect/' + domain + url
            elif not url_parts.scheme:
                return '/redirect/' + domain + '/' + url
            else:
                return url

    try:
        page = requests.get('http://' + site_data[domain] + '/')
    except KeyError:
        return 'No url found for symbol "%s", check ini file.' % domain
    root = lxml.html.fromstring(page.text)
    # #    print 'LINKS BEFORE:', list(root.iterlinks())[-10:]
    root.rewrite_links(replace_url, resolve_base_href=False)
    # #    print 'LINKS AFTER:', list(root.iterlinks())[-10:]
    return lxml.html.tostring(root, method='html', )


@app.route('/redirect/<string:domain>/<path:other>')
def redirect_other(domain, other):
    r = requests.get('http://' + site_data[domain] + '/' + other)
    return r.content
