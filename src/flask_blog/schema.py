import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from . import models
from .types import PostConnection


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    posts = SQLAlchemyConnectionField(PostConnection)

    def resolve_posts(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
        return query.all()


schema = graphene.Schema(query=Query)
