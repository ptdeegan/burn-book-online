from app import app
from src.repositories.post_repository import posts_repository_singlton
from src.models import User_likes, db

def test_burn_count():
    with app.app_context():
        db.session.query(User_likes).delete()
        db.session.commit()
        posts_repository_singlton.like_post(1, 1, True)
        posts_repository_singlton.like_post(2, 1, True)
        posts_repository_singlton.like_post(3, 1, True)

        i =  posts_repository_singlton.get_likes(1)

        assert i == 3