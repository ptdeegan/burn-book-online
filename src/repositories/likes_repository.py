from src.models import Comments, Posts, User_likes, Users, db

class Like_Repository:

    def get_user_likes(self, user_id) -> list[User_likes]:
        all_likes: list[User_likes] = User_likes.query.filter_by(user_id=user_id).all()
        return all_likes

    def delete_like(self, like_id: int):
        del_like: User_likes = User_likes.query.get_or_404(like_id)
        db.session.delete(del_like)
        db.session.commit()


like_repository_singleton = Like_Repository()