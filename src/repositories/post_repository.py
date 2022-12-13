from src.models import Posts, User_likes, db

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
        all_interaction: list[User_likes] = User_likes.query.filter_by(post_id = post_id).all()
        like_total = 0

        for interaction in all_interaction:
            if interaction.is_burn == True:
                like_total += 1
            else:
                like_total -= 1

        return like_total

    def burn_post_check(self, post_id: int):
        #Need to test code still
        i = self.get_likes(post_id)
        if (i > 3):
            modPost = self.get_post_by_id(post_id)
            modPost.post_body = "Burned!"
            db.session.commit()

    #Add post interaction (like or dislike)
    def like_post(self, user_id: int, post_id: int, burn_status: bool) -> User_likes:
        old_interaction: User_likes = User_likes.query.get(user_id, post_id)

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
            new_interaction = User_likes(burn_status, user_id, post_id)
            db.session.add(new_interaction)
            db.session.commit()
            self.burn_post_check(post_id)
            return new_interaction
           
        elif (old_interaction is None):
            #base code that adds new interaction
            new_interaction = User_likes(burn_status, user_id, post_id)
            db.session.add(new_interaction)
            db.session.commit()
            self.burn_post_check(post_id)
            return new_interaction     

    def delete_post(self, post_id: int):
        del_post: Posts = Posts.query.get_or_404(post_id)
        db.session.delete(del_post)
        db.session.commit()

#Singlton for other module use
posts_repository_singlton = Post_Repository()
