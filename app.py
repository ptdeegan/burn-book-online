#!/usr/bin/env python3



from flask import Flask, request, render_template, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from src.repositories.post_repository import posts_repository_singlton
import random 
import os
from dotenv import load_dotenv
from src.models import *

app = Flask(__name__)
pfp_num= random.randrange(0,9)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)

bcrypt = Bcrypt(app)

@app.get('/')
def home():
    #all_posts = posts_repository_singlton.get_all_posts()
    return render_template('index.html')

@app.get('/profile')
def profile():
    return render_template('profile.html', pfp_num=pfp_num)

@app.post('/signup')
def makeProfile():
    username = request.form.get('username')
    password = request.form.get('password')
    dob = request.form.get('dob')
    email = request.form.get('email')
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return redirect('/')

    hashed_bytes = bcrypt.generate_password_hash(password, int(os.getenv('BCRYPT_ROUNDS')))
    hashed_password = hashed_bytes.decode('utf-8')
    new_user = Users(username, first_name, last_name, email, dob, hashed_password)

    db.session.add(new_user) #TODO: DOES NOT POST TO SQL, REMEMBER TO FIX
    db.session.commit()

    return redirect('/')



@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.post('/login')
def letLogin():
    username = request.form.get('username')
    password = request.form.get('password')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/viewpost')
def viewpost():
    return render_template('viewpost.html')