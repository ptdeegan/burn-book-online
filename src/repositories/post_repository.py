from src.models import Posts, User_likes, db
from sqlalchemy import func

class Post_Repository:
    #gets all posts
    def get_all_posts(self) -> list[Posts]:
        all_posts: list[Posts] = Posts.query.all()
        return all_posts

    #gets single post based on ID
    def get_post_by_id(self, post_id: int) -> Posts:
        found_post: Posts = Posts.query.get_or_404(post_id)
        return found_post

    def get_post_by_user(self, user_id: int) -> list[Posts]:
        user_posts: list[Posts] = Posts.query.filter_by(user_id = user_id).all()
        return user_posts

    #create posts
    def create_post(self, user_id: int, title: str, body: str) -> Posts:
        new_post = Posts(user_id, title, body)
        db.session.add(new_post)
        db.session.commit()
        return new_post

    #Sum post interaction and return total
    def get_likes(self, post_id: int) -> int:
        interactions: list[User_likes] = User_likes.query.filter_by(post_id=post_id).all()
        i = 0

        for inter in interactions:
            if inter.is_burn == True:
                i += 1
            else:
                i -= 1

        return i

    def burn_post_check(self, post_id: int):
        #Need to test code still
        i = self.get_likes(post_id)
        if (i > 2):
            modPost = self.get_post_by_id(post_id)
            modPost.post_body = "Burned!"
            db.session.commit()

    #Add post interaction (like or dislike)
    def like_post(self, user_id: int, post_id: int, burn_status: bool) -> User_likes:
        old_interactions: list[User_likes] = User_likes.query.filter_by(post_id=post_id).all()
        old_interaction: User_likes = None
        for i in old_interactions:
            if int(i.user_id) == int(user_id):
                old_interaction = i

        if (old_interaction is None):
            #base code that adds new interaction
            new_interaction = User_likes(user_id, post_id, burn_status)
            db.session.add(new_interaction)
            db.session.commit()
            self.burn_post_check(post_id)
            return new_interaction

        if (old_interaction.is_burn == burn_status):
            #If old interaction is the same as new we will remove the old interaction and return null
            db.session.delete(old_interaction)
            db.session.commit()
            self.burn_post_check(post_id)
            return None

        elif (old_interaction.is_burn != burn_status):
            #If old interaction is not the same as new we will remove old and add new
            db.session.delete(old_interaction)
            db.session.commit()
            new_interaction = User_likes(user_id, post_id, burn_status)
            db.session.add(new_interaction)
            db.session.commit()
            self.burn_post_check(post_id)
            return new_interaction    

    def delete_post(self, post_id: int):
        del_post: Posts = Posts.query.get_or_404(post_id)
        db.session.delete(del_post)
        db.session.commit()

  #Sum all of a users post interaction and returns total
    def get_likes_for_user(self, user_id: int) -> int:
        user_posts: list[user_posts] = Posts.query.filter_by(user_id=user_id)
        user_like_total = 0
        for posts in user_posts:
            all_interaction: list[User_likes] = User_likes.query.filter_by(post_id=posts.post_id).all()
            like_total = 0

            for interaction in all_interaction:
                if interaction.is_burn == True:
                    like_total += 1
                else:
                    like_total -= 1
            user_like_total = user_like_total + like_total
        return user_like_total

#Singlton for other module use
posts_repository_singlton = Post_Repository()
