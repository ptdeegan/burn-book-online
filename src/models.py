from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()





class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(255), nullable = False)
    last_name = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String, nullable = False)
    date_of_birth = db.Column(db.Date, nullable = False)

    def __repr__(self) -> str:
        return f'Users(user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}'

    def __init__(self, first_name: str, last_name: str, email: str, dob: date ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_of_birth = dob

class Posts(db.Model):
    user_id = db.Column(db.Integer, nullable = False)
    post_title = db.Column(db.String(255), nullable = False)
    post_id = db.Column(db.Integer, primary_key = True)
    post_body = db.Column(db.String(255), nullable = False)
    burn_status = db.Column(db.Boolean, nullable = False)

    def __init__(self, user_id: int, title: str, body: str):
        self.user_id = user_id
        self.post_title = title
        self.post_body = body
        self.burn_status = False


