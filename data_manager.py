"""
This module handles all database operations.
"""
from sqlalchemy.exc import SQLAlchemyError
from models import db, User, Movie

class DataManager():
    """
    Handles all database operations.
    """
    def create_user(self,name:str)->None:
        
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error:", e)

    def get_users(self):
        users = User.query.all()
        return users

    def get_movies(self, user_id):
        """Returns a list of all movies for a specific user ID."""
        user = db.session.get(User, user_id)
        if user:
            return user.movies
        return []
    

    def add_movie(self, movie):
        
        try:
            new_movie = Movie(
                title=movie.title, 
                director=movie.director,
                release_year=movie.release_year, 
                poster=movie.poster,
                genre=movie.genre, 
                rating=movie.rating,
                imdb_id=movie.imdb_id,
                countries=movie.countries,
                description=movie.description,
                user_id=movie.user_id
                )
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error:", e)
            return None

    def update_movie(self, movie_id, new_title):
        """
        Updates a movie in the database.
        """
        try:
            movie = db.session.get(Movie, movie_id)
            if movie:
                movie.title = new_title
                db.session.commit()
                return movie
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error:", e)
            return None

    def delete_movie(self, movie_id):
        """
        Deletes a movie from the database.
        """
        try:
            movie = db.session.get(Movie, movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error:", e)
            return False