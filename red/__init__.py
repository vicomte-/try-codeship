from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

if os.environ.get('HEROKU'):
    db_uri = os.environ.get('POSTGRESQL_BLUE_URL')
else:
    from init_this_service import initialize
    db_pwd, site_data = initialize()
    db_uri = 'mysql://vicomte:%s@mysql.server/vicomte$default' % db_pwd
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
print 'DEBUG: dburi=', db_uri

key = os.environ.get('APP_KEY')
if key:
    app.secret_key = key
else:
    app.secret_key = os.urandom(24)
print 'DEBUG: app.secret_key = ', app.secret_key

db = SQLAlchemy(app)
print 'DEBUG: db started =', db

import red.views