from flask.testing import FlaskClient
from app import app
from src.models import Posts, db
from src.repositories.post_repository import posts_repository_singlton

def test_end_to_end(test_app: FlaskClient):
    with app.app_context():
        test_post = posts_repository_singlton.create_post(1, "test_post_name", "test_body")
        db.session.add(test_post)
        db.session.commit()
        
        res = test_app.get("/")
        page_data = res.data.decode()
        
        assert res.status_code == 302
        assert f"<td>{test_post.post_body}</td>"

        db.session.delete(test_post)
        db.session.commit()




        
