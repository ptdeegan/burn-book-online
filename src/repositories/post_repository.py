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

#Singlton for other module use
posts_repository_singlton = Post_Repository()
