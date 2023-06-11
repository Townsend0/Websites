import flask
from datetime import datetime
from flask_bootstrap import Bootstrap
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_gravatar import Gravatar
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from datetime import date
from data import *
from forms import *


load_dotenv()
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap(app)
gravatar = Gravatar(app)
CKEditor(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

session = Session()

email = smtplib.SMTP('smtp.gmail.com', 587)
email.starttls()
email.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))


def admin_required(func):
    @wraps(func)
    
    def decoratd_func(*args, **kwargs):
        
        if not flask_login.current_user.is_authenticated or flask_login.current_user.id != 1:
            return flask.abort(403)
        
        return func(*args, **kwargs)
    return decoratd_func


def check_admin():
    try:
        return flask_login.current_user.id == 1
    
    except AttributeError:
        return False


@login_manager.user_loader
def load_user(id):
    return session.query(Users).get(int(id))


@app.route('/')
def get_all_posts():
    posts = session.query(BlogPost).all()
    
    return flask.render_template("index.html", all_posts=posts, date = date.today().year, 
    logged = flask_login.current_user.is_authenticated, admin = check_admin())


@app.route("/post/<int:post_id>", methods = ['GET', 'POST'])
def show_post(post_id):
    form = CommentSection()
    requested_post = session.query(BlogPost).get(post_id)

    if form.validate_on_submit():
        session.add(Comments(form.comment.data, post_id, flask_login.current_user.name))
        session.commit()
    
    return flask.render_template("post.html", post=requested_post, form = form,
    logged = flask_login.current_user.is_authenticated, admin = check_admin())


@app.route("/about")
def about():
    return flask.render_template("about.html", logged = flask_login.current_user.is_authenticated)


@app.route("/contact", methods = ['POST', 'GET'])
def contact():
    form = Contact()
    if form.validate_on_submit():
        msg = MIMEText(f'We got your message {form.name.data} we will contact you as soon as possible', 'plain', 'utf-8')
        msg['Subject'] = 'Obada\'s Blog'
        msg['From'] = os.getenv('EMAIL')
        msg['To'] = form.email.data
        email.send_message(msg)
        return flask.redirect(flask.url_for('get_all_posts'))
    
    return flask.render_template("contact.html", form = form)


@app.route('/edit-post/<post_id>', methods = ['GET', 'POST'])
@admin_required
def edit_post(post_id):
    a = session.query(BlogPost).filter_by(id = post_id).first()
    form = CreatePostForm(obj = a)
    
    if form.validate_on_submit():
        a.title = form.title.data
        a.author = form.author.data
        a.body = form.body.data
        a.img_url = form.img_url.data
        a.subtitle = form.subtitle.data
        session.commit()
        return flask.redirect(flask.url_for('get_all_posts'))
    
    return flask.render_template('make-post.html', status = 'Edit',
    form = form, logged = flask_login.current_user.is_authenticated)


@app.route('/new-post', methods = ['POST', 'GET'])
@admin_required
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        session.add(BlogPost(form.title.data, datetime.now().strftime('%B %d, %y'),
        form.body.data, form.author.data, flask_login.current_user.id, form.img_url.data, form.subtitle.data))
        session.commit()
    
        return flask.redirect(flask.url_for('get_all_posts'))
    
    return flask.render_template('make-post.html', form = form,
    status = 'New', logged = flask_login.current_user.is_authenticated)


@app.route('/delete/<int:post_id>')
@admin_required
def delete_post(post_id):
    a = session.query(BlogPost).filter_by(id = post_id).first()
    session.delete(a)
    session.commit()
    
    return flask.redirect(flask.url_for('get_all_posts'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = SignIn()
    if form.validate_on_submit():
        
        if not session.query(Users).filter_by(email = form.email.data).first():
            new_user = Users(form.email.data, generate_password_hash(form.password.data, salt_length = 8), form.name.data, gravatar(form.email.data))
            session.add(new_user)
            session.commit()
            flask_login.login_user(new_user)

            return flask.redirect(flask.url_for('get_all_posts'))

        else:
            error = 'You already have an accout related to this email log in instead'
           
            return flask.render_template('register.html', error = error,
            form = form, logged = flask_login.current_user.is_authenticated)
    
    return flask.render_template('register.html', form = form, logged = flask_login.current_user.is_authenticated)


@app.route('/login', methods = ['POST', 'GET'])
def login():
    form = LogIn()

    if form.validate_on_submit():
        user = session.query(Users).filter_by(email = form.email.data).first()
        
        if user and check_password_hash(user.password, form.password.data):
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('get_all_posts'))     
            
        error = 'Check your email and password and try again'
        return flask.render_template('login.html', error = error, form = form, logged = flask_login.current_user.is_authenticated)
    
    return flask.render_template('login.html', form = form, logged = flask_login.current_user.is_authenticated)


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('get_all_posts'))


if __name__ == '__main__':
    app.run(debug = True)
