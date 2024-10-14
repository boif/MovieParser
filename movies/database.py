from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    director = Column(String)
    imdb_rating = Column(Float)
    description = Column(String)

# Настройка базы данных
DATABASE_URL = 'postgresql://boif3x:zipi2281337u@localhost/movies'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()