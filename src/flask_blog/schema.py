import graphene
from graphene import relay


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    ping = graphene.String()

    def resolve_ping(self, info, **kwargs):
        return "pong"


schema = graphene.Schema(query=Query)
