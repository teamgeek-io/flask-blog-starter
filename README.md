# Flask blog starter project

Blog application built with [Flask](https://flask.palletsprojects.com/en/1.1.x/) and [SQLAlchemy](https://www.sqlalchemy.org/).

## Get started

Start by setting up your development environment. First, make sure that you have _Python 3.7.1_ or later available in your terminal. The easiest way to manage multiple versions of _Python_ is to use [pyenv](https://github.com/pyenv/pyenv).

**next, in your project root, install the Python dependencies by executing:**

```
make dev_install
```

**then run the application by executing:\***

```
make run
```

## Linting

To lint your Python code using _flake8_ run:

```
make lint
```

## Testing

Run the automated tests by executing:

```
make test
```

## GraphQL

This starter features a GraphQL API built with [graphene](https://github.com/graphql-python/graphene). To access the GraphiQL of your running server navigate to [http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) in your browser.

### Create a new post

To create a new post via the GraphQL API execute the following mutation in GraphiQL:

```
mutation {
  createPost (input: {
    title: "Test Post"
    content: "Test content"
  }) {
    __typename
    ... on CreatePostSuccess {
      post {
        id
        title
        content
        createdAt
        updatedAt
      }
    }
  }
}
```

### Fetch all posts

To fetch all posts execute the following query in GraphiQL:

```
{
  posts {
    edges {
      node {
        id
        title
        content
        createdAt
      }
    }
  }
}
```
