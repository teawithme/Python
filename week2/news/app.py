#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os, glob
import json
from flask import Flask, render_template, abort

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELAOD'] = True

titles = []
contents = []
ncdict = {}
files = glob.glob('/home/shiyanlou/files/*.json')
#print(files)
for f in files:
    base = os.path.basename(f)
    #print(base)
    with open(f, 'r') as file:
        raw = json.loads(file.read())
        #print(type(raw))
        titles.append(raw["title"])
        contents.append(raw['content'])
        ncdict[os.path.splitext(base)[0]] = raw['content']
#print(titles)
#print(ncdict)
@app.route('/')
def index():
    return render_template('index.html',title=titles)

@app.route('/files/<filename>')
def file(filename):
    content = ncdict.get(filename, 'Invalid')
    if content == 'Invalid':
        abort(404)
    return render_template('file.html', content=content)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
