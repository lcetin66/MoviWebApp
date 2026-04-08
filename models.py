from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.id} {self.name}>'

    def __str__(self):
        return self.name

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, outoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=True)
    release_year = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String, nullable=True)
    genre = db.Column(db.String(20), nullable= True)
    rating = db.Column(db.Float, nullable=False)
    imdb_id = db.Column(db.String, nullable=True)
    countries = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)

    # Link Movie to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Movie {self.id} {self.title}>'

    def __self__(self):
        return self.title
