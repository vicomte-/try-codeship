import os
import base64
from datetime import datetime, timedelta
from flask import session
from collections import deque
from email.utils import parsedate_tz, mktime_tz


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


def clear_and_import_data(data, db, data_object):
    db.drop_all()
    db.create_all()
    count = 0
    for k, v in data.items():
        websites = v
        count += len(websites)
        for site in websites:
            newsite = data_object(**site)
            db.session.add(newsite)
            db.session.commit()
    return "%d Entries imported." % count


def is_it_text(s):
    return isinstance(s, str) or isinstance(s, unicode)


def convert_time_fromstring(verbose):
    return datetime.utcfromtimestamp(mktime_tz(parsedate_tz(verbose)))


def encode_url(url):
    return base64.b64encode(url)


def decode_url(encoded):
    return base64.b64decode(encoded)