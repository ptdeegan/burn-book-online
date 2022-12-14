#!/usr/bin/env python3
from flask import Flask, request, render_template, redirect, session, flash, url_for, abort
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from src.repositories.post_repository import posts_repository_singlton
from src.repositories.comment_repository import Comment_repository_singleton
from src.repositories.profile_repository import profile_repository_singleton
from src.repositories.likes_repository import like_repository_singleton
import random 
import os
from dotenv import load_dotenv
from src.models import *

app = Flask(__name__)
pfp_num= random.randrange(0,9)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SESSION_TYPE'] = 'memcached'
app.secret_key = os.getenv('APP_SECRET_KEY')
db.init_app(app)
bcrypt = Bcrypt(app)

@app.get('/')
def home():
    if 'user' not in session:
        return redirect('/login')
    all_posts = posts_repository_singlton.get_all_posts()
    current_user_info = Users.query.get(session['user']['user_id'])
    pfp_num = session['user']['user_id'] % 10
    return render_template('index.html', posts = all_posts, current_user_info=current_user_info, pfp_num=pfp_num)

@app.get('/profile/<user_id>')
def profile(user_id):
    same_user = False
    if int(user_id) == session["user"]["user_id"]:
        same_user = True
    user_page_info = Users.query.get(user_id)
    current_user_info = Users.query.get(session['user']['user_id'])
    pfp_num = session['user']['user_id'] % 10
    user_posts = Posts.query.filter_by(user_id=user_id).all()
    num_likes = posts_repository_singlton.get_likes_for_user(user_id)
    num_posts = len(posts_repository_singlton.get_post_by_user(user_id))
    return render_template('profile.html', pfp_num=pfp_num, user_page_info = user_page_info, current_user_info=current_user_info, same_user = same_user, user_posts=user_posts, num_likes=num_likes, num_posts=num_posts)

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

    db.session.add(new_user)
    db.session.commit()

    session['user'] = {
    'email': new_user.email,
    'username' : new_user.username,
    'user_id': new_user.user_id,
    }

    uid = new_user.user_id

    return redirect(f'/profile/{uid}')



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
    uid = session['user']['user_id']
    return redirect(f'/profile/{uid}')

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/posts/<post_id>')
def viewpost(post_id: int):
    single_post = posts_repository_singlton.get_post_by_id(post_id)
    post_comments = Comment_repository_singleton.get_comments(post_id)
    user_id = session['user']['user_id']
    current_user_info = Users.query.get(user_id)
    poster = single_post.users.user_id
    num_burns=posts_repository_singlton.get_likes(post_id=post_id)
    same_user = False
    if int(poster) == session["user"]["user_id"]:
        same_user = True

    #if single_post.post_body == "Burned!":
        #burned = True
    return render_template('viewpost.html', current_post=single_post, comments = post_comments, current_user_info=current_user_info, same_user=same_user, num_burns=num_burns, poster=poster)

@app.post('/comment')
def add_comment():
    user_id = session['user']['user_id']
    comment_bod = request.form.get('comment')
    post_id = request.form.get('post_id') 
    new_comment = Comments(user_id=user_id, comment_body=comment_bod, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.get('/signout')
def signout():
    if not session['user']:
        return abort(403)
    del session['user']
    return redirect('/login')

@app.get('/posts/new')
def create_posts_form():
    uid = session['user']['user_id']
    current_user_info = Users.query.get(uid)
    return render_template('create_posts_form.html', current_user_info=current_user_info)

@app.post('/posts')
def create_post():
    title = request.form.get('title', '')
    body = request.form.get('body', '')
    uid = session['user']['user_id']

    posts_repository_singlton.create_post(uid, title, body)
    return redirect('/')

@app.post('/deletepost/<post_id>')
def delete_post(post_id):
    comments = Comment_repository_singleton.get_comments(post_id)
    for comment in comments:
        Comment_repository_singleton.delete_comment(comment.comment_id)
    likes = like_repository_singleton.get_post_likes(post_id)
    for like in likes:
        like_repository_singleton.delete_like(like.like_id)
    posts_repository_singlton.delete_post(post_id)
    return redirect('/')


@app.post('/burnpost/<post_id>')
def burn_post(post_id):
    user_id = request.form.get('user_id')
    posts_repository_singlton.like_post(post_id=post_id, user_id=user_id, burn_status=True)
    return redirect(f'/posts/{post_id}')

@app.post('/dousepost/<post_id>')
def douse_post(post_id):
    user_id = request.form.get('user_id')
    posts_repository_singlton.like_post(post_id=post_id, user_id=user_id, burn_status=False)
    return redirect(f'/posts/{post_id}')

@app.post('/deleteprofile/<profile_id>')
def delete_profile(profile_id):
    user_likes = like_repository_singleton.get_user_likes(profile_id)
    for like in user_likes:
        like_repository_singleton.delete_like(like.like_id)
    user_posts = posts_repository_singlton.get_post_by_user(profile_id)
    for post in user_posts:
        comments = Comment_repository_singleton.get_comments(post.post_id)
        for comment in comments:
            Comment_repository_singleton.delete_comment(comment.comment_id)
        posts_repository_singlton.delete_post(post.post_id)
    profile_repository_singleton.delete_profile(profile_id)
    del session['user']
    return redirect('/')

@app.post('/deletecomment/<comment_id>')
def delete_comment(comment_id):
    post_id = request.form.get('post_id')
    print(post_id)
    Comment_repository_singleton.delete_comment(comment_id)
    return redirect(f'/posts/{post_id}')

@app.post('/edit/<post_id>')
def post_editor(post_id):
    post = Posts.query.get(post_id)
    current_user_info = Users.query.get(session['user']['user_id'])
    return render_template('edit_post.html', post=post, current_user_info=current_user_info)

@app.post('/editpost/<post_id>')
def edit_post(post_id):
    post = Posts.query.get(post_id)
    title = request.form.get('title')
    body = request.form.get('body')
    post.post_body = body
    post.post_title = title
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.get('/editprofile/<user_id>')
def profile_editor(user_id):
    user = Users.query.get(user_id)
    current_user_info = Users.query.get(session['user']['user_id'])
    return render_template('edit_profile.html', user=user, current_user_info=current_user_info)

@app.post('/editprofile/<user_id>')
def edit_profile(user_id):
    user = Users.query.get(user_id)
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    username = request.form.get('username')
    # if Users.query.filter_by(username=username).first():
    #     flash('Account already exists with this username, please try again')
    #     return redirect(f'/editprofile/{user_id}')
    email = request.form.get('email')
    # if Users.query.filter_by(email=email).first():
    #     flash('Account already exists with this email, please try again')
    #     return redirect(f'/editprofile/{user_id}')
    user.firstname = fname
    user.lastname = lname
    user.username = username
    user.email = email
    db.session.commit()
    return redirect(f'/profile/{user_id}')

@app.post('/editcomment/<comment_id>')
def comment_editor(comment_id):
    post_id = request.form.get('post_id')
    comment = Comments.query.get(comment_id)
    post = Posts.query.get(post_id)
    current_user_info = Users.query.get(session['user']['user_id'])
    return render_template('edit_comment.html', comment=comment, current_user_info=current_user_info, post=post)

@app.post('/makeedit/<comment_id>')
def edit_comment(comment_id):
    comment = Comments.query.get(comment_id)
    body = request.form.get('body')
    post_id = request.form.get('post_id')
    comment.comment_body = body
    db.session.commit()
    return redirect(f'/posts/{post_id}')

