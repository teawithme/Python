#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os, glob
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELAOD'] = True

titles = []
contents = []
ncdict = {}
files = glob.glob('~/Documents/python/shiyanlou/week2/files/*.json')
for f in files:
    base = os.path.basename('f')
    with open(f, 'r') as file:
        raw = file.read()
        titles.append(raw['title'])
        contents.append(raw['content'])
        ncdict[os.path.splitext(base)[0]] = raw['content']

@app.route('/')
def index():
    return render_template('index.html',title=title)

@app.route('/files/<filename>')
def file(filename):
    content = contents.get(filename, 'Invalid')
    if content == 'Invalid':
        abort(404)
    return render_template('file.html', content)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
