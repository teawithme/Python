#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import os, glob
import json
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELAOD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/shiyanlou'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    content = db.Column(db.Text)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref='files')

    def __init__(self, title, category, content, created_time):
        self.title = title
        if self.created_time is None:
            self.created_time = datetime.utcnow()
        self.content = content
        self.category = category

    def __repr__(self):
        return '<File %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

#files = glob.glob('/home/shiyanlou/files/*.json')
#print(files)
#for f in files:
#    base = os.path.basename(f)
#    #print(base)
#    with open(f, 'r') as file:
#        raw = json.loads(file.read())
#        #print(type(raw))
#        titles.append(raw["title"])
#        contents.append(raw['content'])
#        ncdict[os.path.splitext(base)[0]] = raw['content']
#print(titles)
#print(ncdict)

@app.route('/')
def index():
    idtdict = {}
    files = File.query.all()
    for file in files:
        id = file.id
        idtdict[id] = file.title
    return render_template('index.html',idtdict=idtdict)

@app.route('/files/<file_id>')
def file(file_id):
    file_filtered = File.query.filter_by(id=file_id).first()
    #if content == 'Invalid':
        #abort(404)
    #print(type(file_filtered))
    #print(file_filtered)
    #print(file_filtered.created_time)
    return render_template('file.html', file_filtered=file_filtered)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
