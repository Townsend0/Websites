from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterForm, LoginForm, CommentForm, PostForm, ContactForm
from .models import Post, Comment
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from smtplib import SMTP
from dotenv import load_dotenv
import os
from email.mime import text

load_dotenv()

def get_all_posts(request):
    return render(request, 'index.html', {'all_posts': Post.objects.all()})


def show_post(request, post_id):
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                comment = request.POST['comment'],
                gravatar_url = f'https://www.gravatar.com/avatar/{request.user.email}?d=identicon&r=PG',
                post_id = post_id,
                user_id = request.user.id,
            )
            return redirect('show_post', post_id = post_id)
    return render(request, 'post.html', {'post': Post.objects.get(id = post_id), 'form': form})


@user_passes_test(lambda a: a.is_superuser)
def edit_post(request, post_id):
    form = PostForm(instance = Post.objects.get(id = post_id))
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.update(
                title = form.cleaned_data['title'],
                subtitle = form.cleaned_data['subtitle'],
                author = form.cleaned_data['author'],
                img_url = form.cleaned_data['img_url'],
                content = form.cleaned_data['content'],
                user = request.user,
            )
            return redirect('get_all_posts')
    return render(request, 'make-post.html', {'form': form, 'purpose': 'Edit'})


@user_passes_test(lambda a: a.is_superuser)
def delete_post(request, post_id):
    Post.objects.get(id = post_id).delete()
    return redirect('get_all_posts')


@user_passes_test(lambda a: a.is_superuser)
def add_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                title = form.cleaned_data['title'],
                subtitle = form.cleaned_data['subtitle'],
                author = form.cleaned_data['author'],
                img_url = form.cleaned_data['img_url'],
                content = form.cleaned_data['content'],
                user = request.user,
            )
            return redirect('get_all_posts')
    return render(request, 'make-post.html', {'form': PostForm(), 'purpose': 'Add'})


@user_passes_test(lambda a: not a.is_authenticated)
def register_user(request):
    form = RegisterForm
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(email = form.cleaned_data['email'])
                messages.error(request, 'You already have an account log in instead')
            except:
                User.objects.create_user(username = form.cleaned_data['username'],
                email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                login(request, authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password']))
                return redirect('get_all_posts')
    return render(request, 'register.html', {'form': form})

 
@user_passes_test(lambda a: not a.is_authenticated)
def login_user(request): 
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email = form.cleaned_data['email'])
                if check_password(form.cleaned_data['password'], user.password):
                    login(request, authenticate(username = user.username, password = form.cleaned_data['password']))
                    return redirect('get_all_posts')
                else:
                    messages.error(request, 'Your email or password is incorrect')
            except:
                messages.error(request, 'Your email or password is incorrect')
    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('get_all_posts')


def about(request):
    return render(request, 'about.html')


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            server = SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))
            msg = text.MIMEText(f'''We have received your message {form.cleaned_data["name"]} and would like to thank you for writing to us we will reply by email as soon as possible''')
            msg['Subject'] = 'Obada Blog'
            msg['To'] = form.cleaned_data['email']
            msg['From'] = os.getenv('EMAIL')
            server.send_message(msg)
            server.quit()
            messages.success(request, 'Your email was sent successfully')
            form = ContactForm()
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})