#!/usr/bin/env python3



from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import random 
import os
from dotenv import load_dotenv
from models import db
db.init_app(app)
app = Flask(__name__)
pfp_num= random.randrange(0,9)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/profile')
def profile():
    return render_template('profile.html', pfp_num=pfp_num)

@app.post('/signup')
def signup():
    username = request.form.get('username')
    password = request.form.get('password')
    dob = request.form.get('dob')
    email = request.form.get('email')

@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/viewpost')
def viewpost():
    return render_template('viewpost.html')