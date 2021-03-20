import json
import traceback

import jwt
from flask import Blueprint, current_app, g, request
from flask_cors import CORS
from flask_graphql import GraphQLView
from werkzeug.exceptions import Forbidden

from ..schema import schema

graphql = Blueprint("graphql", __name__)

CORS(graphql)


class AuthorizationMiddleware:
    def resolve(self, next, root, info, **args):
        if "user" not in g:
            try:
                token = request.headers.get("Authorization")
                if token:
                    payload = jwt.decode(
                        token,
                        current_app.config["JWT_SECRET"],
                        algorithms=["HS256"],
                    )
                    g.user = {
                        "email": payload.get("email"),
                        "family_name": payload.get("family_name"),
                        "given_name": payload.get("given_name"),
                        "phone_number": payload.get("phone_number"),
                    }
                else:
                    g.user = None
            except Exception:
                current_app.logger.exception(
                    f"Invalid authorization token: {token}"
                )
                raise Forbidden()

        return next(root, info, **args)


class ErrorMiddleware:
    def handle_error(self, err):
        tb = getattr(err, "__traceback__", None)
        if tb:
            traceback.print_tb(tb)
        raise err

    def resolve(self, next, root, info, **args):
        return next(root, info, **args).catch(self.handle_error)


graphql.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        middleware=[ErrorMiddleware(), AuthorizationMiddleware()],
        graphiql=True,
    ),
)


@graphql.after_request
def after(response):
    if response.status_code >= 400:
        data = json.loads(response.get_data())
        current_app.logger.error(data)
    return response
