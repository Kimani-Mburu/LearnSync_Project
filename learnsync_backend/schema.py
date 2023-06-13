import graphene

class Query(graphene.ObjectType):
    # Define your GraphQL queries here

    pass

schema = graphene.Schema(query=Query)
