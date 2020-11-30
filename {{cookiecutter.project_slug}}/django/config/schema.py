import graphene
from graphene_django.debug import DjangoDebug
import {{cookiecutter.project_slug}}.users.schema


class Query({{cookiecutter.project_slug}}.users.schema.Query,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation({{cookiecutter.project_slug}}.users.schema.Mutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
