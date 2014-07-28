#!/usr/bin/python
# A very simple Flask Hello World app for you to get started with...
import os
from flask import Flask
# noinspection PyUnresolvedReferences
from flask.ext.sqlalchemy import SQLAlchemy

if os.environ.get('HEROKU'):
    db_uri = os.environ.get('POSTGRESQL_BLUE_URL')
else:
    from init_this_service import initialize

    db_pwd, site_data = initialize()
    db_uri = 'mysql://vicomte:%s@mysql.server/vicomte$default' % db_pwd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
key = os.environ.get('APP_KEY')
if key:
    app.secret_key = key
else:
    app.secret_key = os.urandom(24)
print 'app.secret_key = ', app.secret_key
db = SQLAlchemy(app)

import models
import views

