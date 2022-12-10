from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    first_name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String, nullable = False)
    date_of_birth = db.Column(db.Date, nullable = False)
    admin_status = db.Column(db.Boolean, nullable = False)
    password = db.Column(db.String, nullable = False)
    posts = db.relationship('Posts', backref = db.backref('users', lazy = True))

    def __repr__(self) -> str:
        return f'Users(user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}'

    def __init__(self, username: str, first_name: str, last_name: str, email: str, dob: date, password: str ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = dob
        self.admin_status = False
        self.password = password

class Posts(db.Model):
    __tablename__ = 'posts'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    post_title = db.Column(db.String(255), nullable = False)
    post_id = db.Column(db.Integer, primary_key = True)
    post_body = db.Column(db.String(255), nullable = False)
    burn_status = db.Column(db.Boolean, nullable = False)

    def __init__(self, user_id: int, title: str, body: str):
        self.user_id = user_id
        self.post_title = title
        self.post_body = body
        self.burn_status = False

class User_likes(db.Model):
    __tablename__ = 'user_likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable = False)
    is_burn = db.Column(db.Boolean, primary_key = True)

    def __init__(self, burn: bool, user_id: int, post_id: int):
        self.user_id = user_id
        self.post_id = post_id
        self.is_burn= burn

class Comments(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable = False)
    comment_body = db.Column(db.String, nullable = False)

    def __init__(self, comment_id: int, user_id: int, post_id: int, comment_body: str):
        self.comment_id = comment_id
        self.user_id = user_id
        self.post_id = post_id
        self.comment_body = comment_body

