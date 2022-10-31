#!/usr/bin/env python3

from flask import Flask, request, render_template

app = Flask(__name__)

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/profile')
def profile():
    return render_template('profile.html')
