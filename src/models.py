from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()





class Users(db.Model):
    user_id = db.Column(db.Integer, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

def __repr__(self) -> str:
    return f'Users(user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}'

def __init__(self, user_id:int, first_name:str, last_name:str, email:str ):
    self.user_id = user_id
    self.first_name = first_name
    self.last_name = last_name
    self.email = email



