from django.shortcuts import render, redirect, HttpResponse
from .forms import ContactForm, NewsForm, Search
from .models import Tag, Card, Page, Email
import smtplib
import os
from dotenv import load_dotenv
from django.contrib import messages
from django.core.paginator import Paginator

load_dotenv()

def home(request):
    context = {   
        'design': Card.objects.filter(page__tag__tag = 'design'),
        'marketing': Card.objects.filter(page__tag__tag = 'advertising'),
        'finance': Card.objects.filter(page__tag__tag = 'finance'),
        'music': Card.objects.filter(page__tag__tag = 'music'),
        'education': Card.objects.filter(page__tag__tag = 'education'),
        'form': Search(),
    }
    form = Search()
    if request.method == 'POST':
        form = Search(request.POST)
        if form.is_valid():
            context['results'] = Card.objects.filter(title__icontains = request.POST.get('search'))
            if not context['results']:
                messages.error(request, 'There is no such card in our database')
    
    return render(request, 'index.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
            server.sendmail(os.getenv('EMAIL'), 'obadah2109@gmail.com',
            f'Subject:{form.cleaned_data["subject"]}\n\n{form.cleaned_data["message"]}')
            server.quit()
            messages.success(request, 'Your email was sent successfully')
            form = ContactForm()
            return redirect('home')
    return render(request, 'contact.html', {'form': form})


def detail(request, card_id):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email was saved successfully')
            form = NewsForm()
    return render(request, 'topics-detail.html', {'form': form, 'card': Card.objects.get(id = card_id)})


def listing(request):
    card = Paginator(Card.objects.all(), 3).get_page(request.GET.get('page'))
    card.next_page_number
    context = {'cards': Paginator(Card.objects.all(), 3).get_page(request.GET.get('page'))}
    return render(request, 'topics-listing.html', context)

