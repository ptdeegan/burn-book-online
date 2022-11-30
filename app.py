#!/usr/bin/env python3



from flask import Flask, request, render_template
import random 
import os

app = Flask(__name__)
pfp_num= random.randrange(0,9)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/profile')
def profile():
    return render_template('profile.html', pfp_num=pfp_num)

@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/viewpost')
def viewpost():
    return render_template('viewpost.html')