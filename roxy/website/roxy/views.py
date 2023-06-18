from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages
import phonenumbers
from . import models
from django.core.paginator import Paginator


def home(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                number = phonenumbers.parse(form.cleaned_data['country'] + form.cleaned_data['number'])
                if phonenumbers.is_valid_number(number):
                    new_form = form.save(0)
                    new_form.phone = number
                    new_form.save()
                    messages.success(request, 'Your message was sent successfully', 'success')
                else:
                    messages.error(request, 'Invalid phone number', 'danger')
            except:
                messages.error(request, 'Invalid phone number', 'danger')
        messages.error(request, form.errors, 'danger')

        
    templates = models.Template.objects.all()
    context = {
        'form': form,
        'testimonial': models.Testimonial.objects.order_by('?')[:3],
        'portfolio': models.Portfolio.objects.all(),
        'templates': list([templates[a], templates[a + 1]] for a in range(0, len(templates), 2)),
    }
    
    return render(request, 'index.html', context)


def blog(request):
    cards = Paginator(models.Card.objects.order_by('?').all(), 3)
    return render(request, 'blog.html', {'cards': cards.get_page(request.GET.get('page'))})


def about(request):
    return render(request, 'about.html')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                number = phonenumbers.parse(form.cleaned_data['country'] + form.cleaned_data['number'])
                if phonenumbers.is_valid_number(number):
                    new_form = form.save(0)
                    new_form.phone = number
                    new_form.save()
                    messages.success(request, 'Your message was sent successfully')
                    return redirect('home')
                messages.error(request, 'Invalid phone mumber', 'danger')
            except:
                messages.error(request, 'Invalid phone number', 'danger') 
        messages.error(request, form.errors, 'danger')  
    return render(request, 'contact.html', {'form': form})


def single(request, page_id):
    return render(request, 'single.html', {'page': models.Page.objects.get(id = page_id)})

