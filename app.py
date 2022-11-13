#!/usr/bin/env python3

from flask import Flask, request, render_template
import random 
app = Flask(__name__)
pfp_num= random.randrange(0,9)

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/profile')
def profile():
    return render_template('profile.html', pfp_num=pfp_num)

@app.get('/signup')
def signup():
    return render_template('signup.html')