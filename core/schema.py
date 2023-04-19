import graphene
from graphene_django import DjangoObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.contrib.auth.models import User
from blog.schema import BlogQuery, BlogMutation, PostMutation, PostQuery, CommentQuery

# Define a type for User model
class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ['password']

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


class Query(BlogQuery, PostQuery, CommentQuery, graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(),
                          username=graphene.String())

    # @login_required
    def resolve_users(self, info):
        return User.objects.all()
    
    # @login_required
    def resolve_user(self, info, id=None, username=None):
        if username:
            return User.objects.get(username=username)
        return User.objects.get(id=id)


class Mutation(BlogMutation, PostMutation, graphene.ObjectType):
    create_user = CreateUser.Field()

    # jwt authentication mutations
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
