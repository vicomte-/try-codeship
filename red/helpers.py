import os
import base64
from red import db
from datetime import datetime, timedelta
from flask import session
from collections import deque
from models import Websites

__author__ = 'Surfer'


def brackify(tag):
    return '<%s>' % tag


def taggify(html, tags):
    balanced_tags = deque([html])
    for tag in tags:
        balanced_tags.appendleft(brackify(tag))
        balanced_tags.append(brackify('/%s' % tag))
    return ''.join(balanced_tags)


def mark_as_preformatted(html):
    return taggify(html, ['pre', 'code'])


def calc_expiration():
    timeout = os.environ.get('SESSION_TIMEOUT')
    if not timeout:
        timeout = 100
    else:
        timeout = int(timeout)
    return datetime.now() + timedelta(seconds=timeout)


def check_logged_in():
    if session.get('logged_in'):
        if datetime.now() <= session['expiration']:
            session['expiration'] = calc_expiration()
            return True
    return False


def set_default(check, default):
    if check:
        return check
    else:
        return default


def clear_and_import_data(data):
    db.drop_all()
    db.create_all()
    for k, v in data.items():
        websites = v
        for site in websites:
            for col, val in site.items():
                print '%s-->%s' % (col, val),
            print '\n'
            newsite = Websites(**site)
            db.session.add(newsite)
            db.session.commit()


def encode_url(url):
    return base64.b64encode(url)


def decode_url(encoded):
    return base64.b64decode(encoded)