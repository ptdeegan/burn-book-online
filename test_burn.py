from app import app
from src.repositories.post_repository import posts_repository_singlton
from src.models import User_likes, db

def test_burn_func():
    with app.app_context():
        db.session.query(User_likes).delete()
        db.session.commit()
        posts_repository_singlton.like_post(1, 1, True)
        posts_repository_singlton.like_post(2, 1, True)
        posts_repository_singlton.like_post(3, 1, True)

        p = posts_repository_singlton.get_post_by_id(1)

        assert p.post_body == "Burned!"