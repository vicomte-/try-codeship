from flask import Flask
import os
app = Flask(__name__)

key = os.environ.get('APP_KEY')
if key:
    app.secret_key = key
else:
    app.secret_key = os.urandom(24)
print 'app.secret_key = ', app.secret_key


import red.views