from app import app
from src.repositories.post_repository import posts_repository_singlton

def test_burn():
    with app.app_context():
        x = posts_repository_singlton.like_post(1, 1, True)
        i = posts_repository_singlton.get_likes(1)

        if x is not None: 
            assert i == 1
        else:
            assert i == 0
