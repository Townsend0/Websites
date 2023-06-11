from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField("Blog Post Title", max_length=250)
    subtitle = models.CharField("Subtitle", max_length=250)
    author = models.CharField("Your name", max_length=250)
    content = RichTextField('Blog Content')
    img_url = models.URLField('Blog Image URL')
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    date = models.DateField(auto_now_add = True)

    def __str__(self) -> str:
        return self.title
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'post_comments')
    comment = models.TextField('Comment')
    gravatar_url = models.URLField(null = True, blank = True)
    
    def __str__(self) -> str:
        return self.comment




