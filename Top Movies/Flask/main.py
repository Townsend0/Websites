import flask
from flask_bootstrap import Bootstrap
from forms import *
from database import *
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
Bootstrap(app)


def movies_search(movie_id):
    params = { 'api_key': os.environ['API_KEY']}
    a = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}', params=params).json()
    return {
        'title': a['title'],
        'year': int(a['release_date'].split('-')[0]),
        'review': a['tagline'],
        'img_url': a['poster_path'],
        'rating': round(a['vote_average'], 1),
        'description': a['overview'],
    }
    


def movies_selection(title):
    
    params = { 'api_key': os.environ['API_KEY'], 'query': title }
    a = requests.get(f'https://api.themoviedb.org/3/search/movie?', params= params).json()['results']
    b = list()
    
    for c in a:
        b.append([c['title'], c['release_date'].split('-')[0], c['id']])
        
    return b


@app.route("/")
def home():
    
    try:
        movies = read_database()
        
    except:
        movies = []
        
    return flask.render_template("index.html", movies = movies)


@app.route("/add", methods = ['GET', 'POST'])
def add():
    
    forms = Add()
    
    if forms.validate_on_submit():
        
        return flask.redirect(flask.url_for("select", title = forms.title.data))
    
    return flask.render_template("add.html", forms = forms)


@app.route("/edit/<int:movie_id>", methods = ['GET', 'POST'])
def edit(movie_id):
    
    forms = Edit()
    
    if forms.validate_on_submit():
        edit_row(forms.review.data, forms.rating.data, movie_id)
        
        return flask.redirect(flask.url_for('home'))
    
    return flask.render_template("edit.html", forms = forms)


@app.route("/delete<int:movie_id>")
def delete(movie_id):
    
    delete_row(movie_id)
    return flask.redirect(flask.url_for('home'))
    

@app.route("/select/<title>")
def select(title):
    
    return flask.render_template("select.html", options = movies_selection(title))

@app.route('/added/<int:movie_id>')
def added(movie_id):
    add_to_databse(movies_search(movie_id))
    
    return flask.redirect(flask.url_for('home'))


if __name__ == '__main__':
    app.run(debug = True)
