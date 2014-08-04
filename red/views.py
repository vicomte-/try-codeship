from red import app
import os
from functools import wraps
from helpers import check_logged_in, mark_as_preformatted, calc_expiration
from helpers import set_default
from flask import request, session, flash, url_for, render_template, redirect


@app.route('/')
def index():
    return 'Hello World!'

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

