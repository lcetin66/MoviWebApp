"""
This module contains the database models for the application.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    Represents a user in the database.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the user.
        """
        return f'<User {self.id} {self.name}>'

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return self.name

class Movie(db.Model):
    """
    Represents a movie in the database.
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=True)
    release_year = db.Column(db.Integer, nullable=True)
    poster = db.Column(db.String, nullable=True)
    genre = db.Column(db.String(20), nullable= True)
    rating = db.Column(db.Float, nullable=True)
    imdb_id = db.Column(db.String, nullable=True)
    countries = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the movie.
        """
        return f'<Movie {self.id} {self.title}>'

    def __str__(self):
        """
        Returns a string representation of the movie.
        """
        return self.title
