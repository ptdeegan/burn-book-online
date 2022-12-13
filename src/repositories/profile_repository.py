from src.models import Comments, Posts, User_likes, Users, db

class Profile_Repository:

    def delete_profile(self, profile_id: int):
        del_profile: Users = Users.query.get_or_404(profile_id)
        db.session.delete(del_profile)
        db.session.commit()


profile_repository_singleton = Profile_Repository()