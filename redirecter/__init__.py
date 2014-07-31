#!/usr/bin/python
# A very simple Flask Hello World app for you to get started with...
import os

from flask import Flask

# noinspection PyUnresolvedReferences
from flask.ext.sqlalchemy import SQLAlchemy

if os.environ.get('HEROKU'):
    db_uri = os.environ.get('POSTGRESQL_BLUE_URL')
    print 'DEBUG: starting on heroku'
else:
    from redirecter.init_this_service import initialize

    db_pwd, site_data = initialize()
    db_uri = 'mysql://vicomte:%s@mysql.server/vicomte$default' % db_pwd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
print 'DEBUG: db-uri set to:', db_uri
key = os.environ.get('APP_KEY')
if key:
    app.secret_key = key
else:
    app.secret_key = os.urandom(24)
    print 'DEBUG: new key generated'
print 'app.secret_key = ', app.secret_key
db = SQLAlchemy(app)

# noinspection PyUnresolvedReferences
import redirecter.views
# noinspection PyUnresolvedReferences
import redirecter.models
