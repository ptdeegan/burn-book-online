from src.models import Comments, Posts, User_likes, db

class Comment_Repository:

    def get_comments(self, post_id) -> list[Comments]:
        all_comments: list[Comments] = Comments.query.filter_by(post_id=post_id).all()
        return all_comments
    
    def create_comment(self, user_id: int, post_id: int, body: str) -> Comments:
        new_comment = Comments(user_id, post_id, body)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment


Comment_repository_singleton = Comment_Repository()