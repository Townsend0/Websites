from django import forms
from .models import MovieData


class SearchForm(forms.Form):
    search = forms.CharField(max_length = 100, widget = forms.TextInput({'placeholder': 'Type the movie\'s name'}))
    
class EditForm(forms.ModelForm):
    class Meta:
        model = MovieData
        fields = ('review', 'rating')

