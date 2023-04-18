import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from blog.schema import BlogQuery, BlogMutation, PostMutation, PostQuery

# Define a type for User model
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"

# Define an input class for User creation
class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)

# Define a mutation class for User creation
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        input = UserInput(required=True)

    def mutate(self, info, input):
        user = User.objects.create_user(**input)
        return CreateUser(user=user)


class Query(BlogQuery, PostQuery, graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(),
                          username=graphene.String())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id=None, username=None):
        if username:
            return User.objects.get(username=username)
        return User.objects.get(id=id)


class Mutation(BlogMutation, BlogQuery, graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
