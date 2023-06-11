from django import forms
from django.contrib.auth.models import User
from .models import Comment, Post

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'username')
        widgets = {
            'email': forms.EmailInput({'class': 'form-control'}),
            'password': forms.PasswordInput({'class': 'form-control'}),
            'username': forms.TextInput({'class': 'form-control'}),
        }
        help_texts = {
            'username': None,
        }
        
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput({'class': 'form-control'}),
            'password': forms.PasswordInput({'class': 'form-control'}),
        }
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea({"class": "form-control"})
        }
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': forms.Textarea({'class': 'form-control'}),
            'title': forms.TextInput({'class': 'form-control'}),
            'subtitle': forms.TextInput({'class': 'form-control'}),
            'author': forms.TextInput({'class': 'form-control'}),
            'img_url': forms.TextInput({'class': 'form-control'}),
        }
        
        
class ContactForm(forms.Form):
    email = forms.EmailField(widget = forms.EmailInput({'placeholder': 'Email', 'class': 'form-control'}))
    name = forms.CharField(widget = forms.TextInput({'placeholder': 'Name', 'class': 'form-control'}))
    message = forms.CharField(widget = forms.Textarea({'placeholder': 'Message', 'class': 'form-control'}))