from django import forms
import pandas
from website.settings import BASE_DIR
from django.forms import widgets
from .models import Contact
from phonenumber_field.widgets import *

file = pandas.read_csv(BASE_DIR / 'roxy/static/files/calling_codes.csv', dtype = {'Country Code': str, 'Country Name': str})
COUNTRY_CODES = set((file['Country Code'][a], file['Country Name'][a]) for a in range(len(file)))

class ContactForm(forms.ModelForm):
    class Meta: 
        model = Contact
        fields = ('name', 'email', 'website', 'message', 'phone')
        widgets = {
            'name': widgets.TextInput({'placeholder': 'Name', 'class': 'form-control'}),
            'email': widgets.EmailInput({'placeholder': 'Email', 'class': 'form-control'}),
            'website': widgets.URLInput({'placeholder': 'Website', 'class': 'form-control'}),
            'message': widgets.Textarea({'placeholder': 'Your Message ...', 'class': 'form-control', 'rows': '6'}),
        }
    country = forms.ChoiceField(choices = COUNTRY_CODES, widget = widgets.Select({'class': 'form-control'}))
    number = forms.CharField(widget = widgets.Input({'class': 'form-control', 'placeholder': 'Phone number'}))

    

    