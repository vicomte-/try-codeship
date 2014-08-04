from red import app, db
import os
import requests
import lxml.html
from functools import wraps
from flask import request, session, flash, url_for, render_template, redirect
from urllib import unquote_plus
from urlparse import urlsplit
from helpers import check_logged_in, mark_as_preformatted, calc_expiration
from helpers import set_default
from models import Websites

@app.route('/')
def index():
    return 'Hello from Flask! minimal R Version 2014-08-04#1 '

@app.route('/default')
def default():
    return 'Hello! This is the default page'

@app.route('/hello/<name>')
def hi(name):
    return 'Hello %s!' % name


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_logged_in():
            return login()
        return f(*args, **kwargs)

    return decorated


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
    print 'DEBUG: entered show_env'
    env_settings = sorted(os.environ.items())
    html = '\n'.join(('%s = %s' % (k, v) for k, v in env_settings))
    return mark_as_preformatted(html)

@app.route('/sites')
@requires_auth
def show_sites():
    print 'DEBUG: db-conn-str', app.config.get('SQLALCHEMY_DATABASE_URI')
    print 'DEBUG: Websites', Websites
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

@app.route('/debug_switch')
def switch_debug():
    debug_status = app.debug
    print 'debug was %s' % debug_status
    app.debug = not debug_status
    print 'debug set to %s' % app.debug
    return 'debug_status switched, now %s' % app.debug


@app.route('/dbcreate')
@requires_auth
def dbcreate():
    db.create_all()
    return 'database created'

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
        website_data = Websites.query.filter_by(label=domain).first()
        page = requests.get('http://' + website_data.url + '/')
    except KeyError:
        return 'No url found for symbol "%s", check ini file.' % domain
    root = lxml.html.fromstring(page.text)
    # #    print 'LINKS BEFORE:', list(root.iterlinks())[-10:]
    root.rewrite_links(replace_url, resolve_base_href=False)
    # #    print 'LINKS AFTER:', list(root.iterlinks())[-10:]
    return lxml.html.tostring(root, method='html', )


@app.route('/redirect/<string:domain>/<path:other>')
def redirect_other(domain, other):
    website_data = Websites.query.filter_by(label=domain).first()
    r = requests.get('http://' + website_data.url + '/' + other)
    return r.content

