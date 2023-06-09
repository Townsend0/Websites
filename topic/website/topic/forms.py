from django import forms
from .models import Email


class ContactForm(forms.Form):
    name = forms.CharField(label = 'Name', widget = forms.TextInput(
    {'class': 'form-control', 'placeholder': 'Name', 'for': 'floatingInput'}))
    
    email = forms.EmailField(label = 'Email address', widget = forms.EmailInput(
    {'class': 'form-control', 'placeholder': 'Email address', 'for': 'floatingInput'}))
    
    subject = forms.CharField(label = 'Subject', widget = forms.TextInput(
    {'class': 'form-control', 'placeholder': 'Subject', 'for': 'floatingInput'}))
    
    message = forms.CharField(label = 'Tell me about the project', widget = forms.Textarea(
        {'class': 'form-control', 'placeholder': 'Tell me about the project', 'for': 'floatingInput'}))
    
    
class NewsForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput({'placeholder': 'Email Address', 'class': 'form-control', 'id': 'subscribe-email'}),
        }
        
        
class Search(forms.Form):
    search = forms.CharField(label = 'Search', widget = forms.TextInput({'name': 'search',
    'placeholder': 'Design, Code, Marketing, Finance ...', 'class': 'form-control', 'type': 'search', }))
    
    
        