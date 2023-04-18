import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Blog, Post, Comment

# a graphql type for the blog model
class BlogType(DjangoObjectType):
    class Meta:
        model = Blog
        fields = "__all__"

# Define a type for Post model
class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"

# Define a type for Comment model
class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = "__all__"

# Define an input class for Post creation
class PostInput(graphene.InputObjectType):
    blog_id = graphene.Int(required=True)
    title = graphene.String(required=True)
    content = graphene.String(required=True)

# a graphql mutation class for creating a blog
class CreateBlog(graphene.Mutation):
    blog = graphene.Field(BlogType)

    class Arguments:
        # the input arguments for the mutation
        name = graphene.String(required=True)

    def mutate(self, info, name):
        # the logic for creating a blog
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to create a blog.")
        blog = Blog(name=name, owner=user)
        blog.save()
        return CreateBlog(blog=blog)

# Define a mutation class for Post creation
class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        input = PostInput(required=True)

    def mutate(self, info, input):
        blog = Blog.objects.get(id=input.blog_id)
        # Check if the blog exists
        if blog:
            # Check if the user is logged in
            if info.context.user.is_authenticated:
                # If yes, assign the user to the post
                user = info.context.user
                post = Post.objects.create(
                    blog=blog, title=input.title, content=input.content, user=user)
                return CreatePost(post=post)
            else:
                # If no, raise an exception with a message
                raise Exception("You must be logged in to create a post.")
        else:
            raise Exception("Blog with the given id does't exists!")

# a graphql mutation class for updating a blog
class UpdateBlog(graphene.Mutation):
    blog = graphene.Field(BlogType)

    class Arguments:
        # the input arguments for the mutation
        id = graphene.Int(required=True)
        name = graphene.String()

    def mutate(self, info, id, name=None):
        # the logic for updating a blog
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to update a blog.")
        blog = Blog.objects.get(id=id)
        if user != blog.owner:
            raise Exception("You can only update your own blog.")
        if name is not None:
            blog.name = name
            blog.save()
        return UpdateBlog(blog=blog)

# a graphql mutation class for deleting a blog
class DeleteBlog(graphene.Mutation):
    message = graphene.String()

    class Arguments:
        # the input arguments for the mutation
        id = graphene.Int(required=True)

    def mutate(self, info, id):
        # the logic for deleting a blog
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to delete a blog.")
        blog = Blog.objects.get(id=id)
        if user != blog.owner:
            raise Exception("You can only delete your own blog.")
        blog.delete()
        return DeleteBlog(message="Blog deleted successfully.")

# a graphql query class for the blog model
class BlogQuery(graphene.ObjectType):
    blogs = graphene.List(
        BlogType, username=graphene.String(), title=graphene.String())
    blog = graphene.Field(BlogType, id=graphene.Int())

    def resolve_blogs(self, info, username=None, title=None):
        # If username is given, filter by author's username
        if username:
            return Blog.objects.filter(owner__username=username)
        # If title is given, filter by title (case insensitive)
        if title:
            return Blog.objects.filter(name__icontains=title)
        # Otherwise, return all blogs
        return Blog.objects.all()

    def resolve_blog(self, info, id):
        # get a specific blog by id
        if Blog.objects.filter(pk=id).first() is None:
            raise Exception(f"Blog with the provided id:{id} id does not exists!")
        return Blog.objects.get(id=id)

# Define a query class for Post model
class PostQuery(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(required=True))

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post(self, info, id):
        return Post.objects.get(id=id)

# Define a query class for Comment model
class CommentQuery(graphene.ObjectType):
    comments = graphene.List(CommentType)
    comment = graphene.Field(CommentType, id=graphene.ID(required=True))

    def resolve_comments(self, info):
        return Comment.objects.all()
    
    def resolve_comment(self, info, id):
        return Comment.objects.get(pk=id)

class CreateComment(graphene.Mutation):
    pass


class UpdateComment(graphene.Mutation):
    pass

class DeleteComment(graphene.Mutation):
    pass

# Define a mutation class for Comment mdoel
class CommentMutation(graphene.ObjectType):
    pass

# Define a mutation class for Post model
class PostMutation(graphene.ObjectType):
    create_post = CreatePost.Field()

# a graphql mutation class for the blog model
class BlogMutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    update_blog = UpdateBlog.Field()
    delete_blog = DeleteBlog.Field()
