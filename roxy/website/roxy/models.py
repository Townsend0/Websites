from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField


class Tag(models.Model):
    choices = (
        ('CODE', 'CODE'),
        ('SPORTS', 'SPORTS'),
        ('ECONOMY', 'ECONOMY'),
    )
    choice = models.CharField(max_length = 250, choices = choices)
    
    def __str__(self):
        return self.choice


class Contact(models.Model):
    name = models.CharField(max_length = 250)
    email = models.EmailField(unique = True)
    website = models.URLField(null = True, blank = True)
    message = models.TextField()
    phone = PhoneNumberField(null = True, blank = True)
    
    def __str__(self):
        return self.name 
    

class Page(models.Model):
    title = models.CharField(max_length = 250)
    content = RichTextField()
    img = models.ImageField(null = True, blank = True, upload_to = 'page')
    
    def __str__(self):
        return self.title


class Card(models.Model):
    page = models.OneToOneField('Page', models.CASCADE)
    date = models.DateField(auto_now_add = True)
    img = models.ImageField(upload_to = 'card')
    tag = models.ManyToManyField('Tag')
    content = models.TextField(max_length = 250)
    by = models.CharField(max_length = 50)
    twitter = models.URLField(null = True, blank = True)
    facebook = models.URLField(null = True, blank = True)
    
    def __str__(self):
        return str(self.page)
    
    
class Testimonial(models.Model):
    name = models.CharField(max_length = 50)
    job = models.CharField(max_length = 50)
    img = models.ImageField(upload_to = 'testimonial', default = 'testimonial/default.png', null = True, blank = True)
    testimony = RichTextField()
    
    
class Portfolio(models.Model):
    
    choices = (
        ('Vintage', 'Vintage'),
        ('Creative', 'Creative'),
        ('Minimalism', 'Minimalism'),
    )
    
    choice = models.CharField(max_length = 50, choices = choices)
    img = models.ImageField(upload_to = 'portfolio')
    description = models.CharField(max_length = 50, default = 'Default')
    
    def __str__(self):
        return self.description
    
    
class Template(models.Model):
    symbol = models.CharField(max_length = 50)
    title = models.CharField(max_length = 50)
    content = models.TextField()
    
    def __str__(self) -> str:
        return self.title

