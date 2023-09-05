# from my_app.models import User, Post, Comment, Like

user = User.objects.create(name="Alex", age=35, gender="male")
user = User.objects.create(name="Ann", age=30, gender="female")
user = User.objects.create(name="Kate", age=25, gender="female")


post1_Alex = Post.objects.create(title="Alex's first post", description="Alex's first description", user=first_user)
post2_Alex = Post.objects.create(title="Alex's second post", description="Alex's second description", user=first_user)
post1_Kate = Post.objects.create(title="Kate's first post", description="Kate's first description", user=third_user)


comment_Alex = Comment.objects.create(title="Alex's first comment", user=User_Alex, post=post1_Alex)
comment2_Alex = Comment.objects.create(title="Alex's second comment", user=User_Alex, post=post1_Alex)
comment1_Kate = Comment.objects.create(title="Kate's first comment", user=User_Kate, post=post1_Kate)
comment2_Kate = Comment.objects.create(title="Kate's second comment", user=User_Kate, post=post1_Kate)
comment3_Kate = Comment.objects.create(title="Kate's third comment", user=User_Kate, post=post1_Kate)


posts = Post.objects.filter(user__name__istartswith="a", user__name__endswith="x")
result = posts.order_by("-title")


comments_all = Comment.objects.all()[0]
del_comment = Comment.objects.filter(pk=1).delete()
new_comment = Comment.objects.create(pk=1, title="New comment", user=User_Alex, post=post2_Alex)


comments_all = Comment.objects.all()
last_comment = comments_all.last()































