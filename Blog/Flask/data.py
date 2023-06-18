import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from flask_login import UserMixin


load_dotenv()
engine = sqlalchemy.create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(engine)
Base = declarative_base()

class Users(Base, UserMixin):
    __tablename__ = 'users'
    
    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key = True)
    email = sqlalchemy.Column(sqlalchemy.String(1000), unique = True)
    password = sqlalchemy.Column(sqlalchemy.String(1000))
    name = sqlalchemy.Column(sqlalchemy.String(1000), unique = True)
    posts = relationship("BlogPost")
    img = sqlalchemy.Column(sqlalchemy.String(1000)) 
    
    def __init__(self, email, password, name, img):
        self.email = email
        self.password = password
        self.name = name
        self.img = img
        
        
class BlogPost(Base):
    __tablename__ = 'posts'
    
    id = sqlalchemy.Column(sqlalchemy.Integer() , primary_key = True)
    title = sqlalchemy.Column(sqlalchemy.String(1000), unique = True)
    date = sqlalchemy.Column(sqlalchemy.String(1000))
    body = sqlalchemy.Column(sqlalchemy.String(10000))
    author = sqlalchemy.Column(sqlalchemy.String(1000))
    img_url = sqlalchemy.Column(sqlalchemy.String(1000))
    subtitle = sqlalchemy.Column(sqlalchemy.String(1000))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    comments = relationship("Comments")
    users = relationship('Users')

    
    def __init__(self, title, date, body, author, author_id, img_url, subtitle):
        self.title = title
        self.date = date
        self.body = body
        self.author = author
        self.author_id = author_id
        self.img_url = img_url
        self.subtitle = subtitle
        
        
class Comments(Base):
    __tablename__ = 'comments'
    
    id = sqlalchemy.Column(sqlalchemy.Integer(), primary_key = True)
    comment = sqlalchemy.Column(sqlalchemy.String(1000))
    post_id = sqlalchemy.Column(sqlalchemy.Integer(), sqlalchemy.ForeignKey('posts.id'))
    user_name = sqlalchemy.Column(sqlalchemy.String(1000), sqlalchemy.ForeignKey('users.name'))
    user = relationship('Users')
    
    def __init__(self, comment, post_id, user_name):
        self.comment = comment
        self.post_id = post_id
        self.user_name = user_name

Base.metadata.create_all(engine)        
