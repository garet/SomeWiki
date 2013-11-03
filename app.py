'''
Created on 01 нояб. 2013 г.

@author: garet
'''

import json
 
from flask import Flask
from flask import redirect
from flask import request
from flask import url_for
from flask import render_template

app = Flask(__name__)


@app.route('/ajax/', defaults={'path': ''})
@app.route('/ajax/<path:path>')
def ajax_handler(path):
    return json.dumps(['<p>Hello!</p>'])

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def urls_handler(path):
    return '<p>Hello!</p>'


if __name__ == '__main__':
    app.debug = True
    app.run()