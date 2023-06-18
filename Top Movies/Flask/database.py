import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:pass123$@localhost/Books')
Session = sessionmaker(engine)

class MoviesData(Base):
    __tablename__ = 'moviesdata'
    
    id = sqlalchemy.Column('id', sqlalchemy.Integer(), primary_key = True)
    title = sqlalchemy.Column('title', sqlalchemy.String(500))
    year = sqlalchemy.Column('year', sqlalchemy.Integer())
    description = sqlalchemy.Column('description', sqlalchemy.String(1000))
    rating = sqlalchemy.Column('rating', sqlalchemy.Float())
    ranking = sqlalchemy.Column('ranking', sqlalchemy.Integer())
    review = sqlalchemy.Column('review', sqlalchemy.String(500))
    img_url = sqlalchemy.Column('img_url', sqlalchemy.String(500))
        
    def __init__(self, title, year, description, rating, review, img_url):
        self.title = title 
        self.year = year
        self.description = description
        self.rating = rating
        self.review = review
        self.img_url = img_url

def add_to_databse(dict):
    Base.metadata.create_all(engine)
    new_user = MoviesData(dict['title'], dict['year'], dict['description'],
    dict['rating'], dict['review'], dict['img_url'])
    session = Session()
    session.add(new_user)
    session.commit()
    session.close()


def read_database():
    session = Session()
    rank()
    return session.execute(sqlalchemy.text('SELECT * FROM books.moviesdata'))

def edit_row(review, rating, movie_id):
    session = Session()
    a = session.query(MoviesData).get(movie_id)
    a.rating, a.review = rating, review
    session.commit()
    session.close()

    
def delete_row(row_id):
    session = Session()
    session.delete(session.query(MoviesData).get(row_id))
    session.commit()
    session.close()    
  
    
def rank():
    session = Session()
    a = session.query(MoviesData).order_by(MoviesData.rating).all()
    
    for b in range(len(a)):
        a[b].ranking = len(a) - b
    
    session.commit()
    session.close()       