from flask_blog import create_app
from flask_blog.database import db
from flask_blog.models import Post


def run():
    app = create_app()
    with app.app_context():
        post = Post(title="First Post", content="Content for the first post")
        post = Post(title="Second Post", content="Content for the second post")

        db.session.add(post)
        db.session.commit()


if __name__ == "__main__":
    run()
