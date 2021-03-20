import flask

from flask_blog import models
from flask_blog.database import db

NO_POSTS_MESSAGE = b"No posts here so far."


def test_empty_db(client):
    rv = client.get("/")
    assert NO_POSTS_MESSAGE in rv.data


def test_create_post(app_context, client):
    title = "Test Post"
    content = "This is a test"
    rv = client.post(
        "/create",
        data=dict(title=title, content=content),
        follow_redirects=True,
    )
    assert flask.request.path == "/"
    assert NO_POSTS_MESSAGE not in rv.data
    assert title.encode() in rv.data

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == title
    assert posts[0].content == content


def test_edit_post(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/edit",
        data=dict(title="New Title", content="New content"),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == "New Title"
    assert posts[0].content == "New content"


def test_delete_post(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/delete",
        data=dict(),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 0
