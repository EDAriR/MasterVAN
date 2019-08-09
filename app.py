# !/usr/local/bin/python
# coding=utf-8
import json
import os
import random
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
from stop_words import stops

import nltk

# 第一次需要
nltk.download('punkt')

from collections import Counter
import operator


app = Flask(__name__)

app.config['DEBUG'] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://hqasllswcsecib:02f2b7a045005e8c3fe69925f190c6f5d72891424058f1163573084d2f7f7fa2@ec2-54-83-50-145.compute-1.amazonaws.com:5432/d2fqdavuf66kvo'
# app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result

#
'''
Authorization: Client-ID YOUR_CLIENT_ID

For accessing a user's account, please visit the OAuth2 section of the docs.

Client ID:

20cc2bbc80fad20
Client secret:
fe5e12a2cc98177b72b9bb6aa18e5ba3d31b6b10
'''
client_id = '20cc2bbc80fad20'
client_secret = 'ee6722fda3d87c73f9336d050e42342495eb23af'
album_id = ''


# from models import Result


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == "POST":
        # get url that the person has entered
        try:
            url = request.form['url']
            r = requests.get(url)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            return render_template('index.html', errors=errors)
        if r:
            # text processing
            raw = BeautifulSoup(r.text, 'html.parser').get_text()
            nltk.data.path.append('./nltk_data/')  # set the path
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            # remove punctuation, count raw words
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)
            # stop words
            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)
            # save the results
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
    return render_template('index.html', errors=errors, results=results)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)
