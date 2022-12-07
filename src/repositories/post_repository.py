from src.models import Posts, db

class Post_Repository:
    #gets all posts
    def get_all_posts(self) -> list[Posts]:
        all_posts = list[Posts] = Posts.query.all()
        return all_posts

    #gets single post based on ID
    def get_post_by_id(self, post_id: int) -> Posts:
        found_post : Posts = Posts.query.get_or_404(post_id)
        return found_post

    def create_post(self, user_id: int, title: str, body: str) -> Posts:
        new_post = Posts(user_id, title, body)
        db.session.add(new_post)
        db.session.commit()
        return new_post

#Singlton for other module use
posts_repository_singlton = Post_Repository()
