#!/usr/bin/env python3

from flask import Flask, request, render_template

app = Flask(__name__)

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/profile')
def profile():
    # will need to fetch all post with users name while they are logged in
    # Could fetch based on a User ID tied to their profile
    return render_template('profile.html')

@app.get('/feed')
def viewpost():
    return render_template('viewpost.html')