from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Blog(models.Model):
    # a blog has a name, an owner, a rating and a set of users who rated it
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[
                                 MinValueValidator(1), MaxValueValidator(5)])
    raters = models.ManyToManyField(
        User, related_name='rated_blogs', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    # a post belongs to a blog and has a title, content, a publication date, a user who posted it, a number of likes and a set of users who liked it
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    likes = models.IntegerField(default=0)
    likers = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    # a comment belongs to a post and has an author, text, a creation date and a user who commented
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    # author = models.CharField(max_length=50)/
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text
