import graphene
from graphene import relay

from .. import models, types
from ..database import db


class CreatePostInput:
    title = graphene.String(required=True)
    content = graphene.String(required=True)


class CreatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class CreatePostOutput(graphene.Union):
    class Meta:
        types = (CreatePostSuccess,)


class CreatePost(relay.ClientIDMutation):
    Input = CreatePostInput
    Output = CreatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        new_post = models.Post(**input)

        db.session.add(new_post)
        db.session.commit()

        return CreatePostSuccess(post=new_post)
