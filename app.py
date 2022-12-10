#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_session import Session
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
app.config['SESSION_TYPE'] = 'memcached'
app.secret_key = os.getenv('APP_SECRET_KEY')
db.init_app(app)
bcrypt = Bcrypt(app)
# Session(app)
sess = Session()

@app.get('/')
def home():
    #if not session.get('user'):
        #return redirect('/login')
    
    all_posts = posts_repository_singlton.get_all_posts()
    return render_template('index.html', posts = all_posts)

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
    
    print(username, password, dob, email, first_name, last_name)

    existing_user = Users.query.filter_by(username=username).first()
    existing_email = Users.query.filter_by(email=email).first()

    if existing_user:
        flash("This username is already being used. Please try a new username.")
        return redirect('/signup')

    if existing_email:
        flash("This email is already in use. Please use a new email.")
        return redirect('/signup')

    hashed_bytes = bcrypt.generate_password_hash(password, int(os.getenv('BCRYPT_ROUNDS')))
    hashed_password = hashed_bytes.decode('utf-8')
    new_user = Users(username=username, first_name=first_name, last_name=last_name, email=email, dob=dob, password=hashed_password)

    db.session.add(new_user) #TODO: unique username unique email message alert, passwords match, redirect message, add pfp
    db.session.commit()

    return redirect('/profile')



@app.get('/signup')
def signup():
    return render_template('signup.html')

@app.post('/login')
def letLogin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()

    if not user:
        flash("Incorrect username. Please retry login.")
        return redirect('/login')
    
    if not bcrypt.check_password_hash(user.password, password):
        flash("Incorrect password. Please retry login.")
        return redirect('/login')
    
    session['user'] = {
    'email': user.email,
    'username' : user.username,
    'user_id': user.user_id,
}
    return redirect('/profile')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/viewpost')
def viewpost():
    return render_template('viewpost.html')