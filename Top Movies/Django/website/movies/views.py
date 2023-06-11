from django.shortcuts import render, redirect
from .forms import SearchForm, EditForm
from dotenv import load_dotenv
import requests
import os
from .models import MovieData
from django.contrib import messages

load_dotenv()

def sort_db():
    data = MovieData.objects.order_by('-rating')
    for a in range(len(data)):
        data[a].ranking = a + 1
        data[a].save()


def home(request):
    sort_db()
    return render(request, 'index.html', {'forms': MovieData.objects.order_by('-rating')})

def add(request):
    
    if len(MovieData.objects.all()) == 10:
        messages.error(request, 'You already have 10 movies on your list')
        return redirect('home')
    
    else:
        form = SearchForm()
        
        if request.method == 'POST':
            form = SearchForm(request.POST)
            
            if form.is_valid():
                url = f'https://api.themoviedb.org/3/search/movie?api_key={os.getenv("API_KEY")}&query={form.cleaned_data["search"]}'
                movies = list()
               
                for a in requests.get(url).json()['results']:
                    movie = ''.join(f'{a["original_title"]} - {a["release_date"].split("-")[0]}')
                    movies.append({"movie": movie, 'id': a['id']})
                
                return render(request, 'select.html', {'movies': movies})
            
    return render(request, 'add.html', {'form': form})

def select(request, movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv("API_KEY")}'
    movie = requests.get(url).json()
    
    MovieData.objects.create(
        title = movie['original_title'],
        year = movie['release_date'].split('-')[0],
        description = movie['overview'],
        rating = movie['vote_average'],
        img_url = f'https://image.tmdb.org/t/p/original{movie["poster_path"]}',
    )
    
    sort_db()
    messages.success(request, f'{movie["original_title"]} was successfully added to your list')
    return redirect('home') 

def update(request, id):
    movie = MovieData.objects.get(id = id)
    form = EditForm(instance = movie)
    
    if request.method == 'POST':
        form = EditForm(request.POST)

        if form.is_valid():
            movie.review = form.cleaned_data['review']
            movie.rating = form.cleaned_data['rating']
            movie.save()
            messages.success(request, f'{movie.title} was successfully edited')
            return redirect('home')
            
    return render(request, 'edit.html', {'form': form})

def delete(request, id):
    movie = MovieData.objects.get(id = id)
    movie_name = movie.title
    movie.delete() 
    sort_db()
    messages.success(request, f'{movie_name} was successfully deleted from your list')
    return redirect('home')