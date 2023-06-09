from django.db import models


class Card(models.Model):
    title = models.CharField(max_length = 250)
    subtitle = models.CharField(max_length = 250)
    number = models.PositiveSmallIntegerField()
    page = models.OneToOneField('Page', on_delete = models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Tag(models.Model):
    tags = (
        ('design', 'Design'),
        ('finance', 'Finance'),
        ('music', 'Music'),
        ('education', 'Education'),
        ('advertising', 'Marketing'),
    )
    tag = models.CharField(max_length = 250, choices = tags)
    
    def __str__(self) -> str:
        return self.tag
    
    
class Page(models.Model):
    intro = models.CharField(max_length = 250)
    title = models.CharField(max_length = 250)
    body1 = models.TextField()
    img = models.ImageField()
    img1 = models.ImageField(null = True, blank = True, )
    img2 = models.ImageField(null = True, blank = True, )
    quote = models.CharField(null = True, blank = True, max_length = 250)
    body2 = models.TextField(null = True, blank = True)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.intro

class Email(models.Model):
    email = models.EmailField(unique = True)
    
    def __str__(self):
        return self.email