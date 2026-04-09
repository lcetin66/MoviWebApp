import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from data_manager import DataManager
from models import db, User, Movie

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['OMDB_API_KEY'] = os.getenv('OMDB_API_KEY')

# Database configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, "data", "movies.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
data_manager = DataManager()


def fetch_movie_info(title):
    """Fetches movie details from OMDB API with robust error handling."""
    api_key = app.config.get('OMDB_API_KEY')
    base_url = "http://www.omdbapi.com/"
    params = {
        'apikey': api_key,
        't': title,
        'plot': 'short'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status() # Catches HTTP errors (404, 500, etc.)
        data = response.json()
        
        if data.get('Response') == 'True':
            rating_str = data.get('imdbRating', '0.0')
            try:
                rating = float(rating_str)
            except ValueError:
                rating = 0.0

            return {
                'title': data.get('Title'),
                'director': data.get('Director'),
                'release_year': int(data.get('Year', '0')[:4]) if data.get('Year') else 0,
                'poster': data.get('Poster'),
                'genre': data.get('Genre'),
                'rating': rating,
                'imdb_id': data.get('imdbID'),
                'countries': data.get('Country'),
                'description': data.get('Plot')
            }
    except requests.exceptions.RequestException as e:
        # Catch and print any API-related errors
        print(f"API Error Occurred: {str(e)}")
        
    return None


@app.route('/')
def home():
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_user_movies(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return "User not found", 404
    
    movies = data_manager.get_movies(user_id)
    print(f"DEBUG: Found {len(movies)} movies for user {user.name}.")
    return render_template('movies.html', user=user, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    title = request.form.get('title')
    form_year = request.form.get('year')
    form_rating = request.form.get('rating')
    
    # Safe conversion for empty strings
    year = int(form_year) if form_year and form_year.strip() else 0
    rating = float(form_rating) if form_rating and form_rating.strip() else 0.0
    
    # Fetch info from OMDB
    movie_info = fetch_movie_info(title) or {}
    
    # Merge API data with fallback to form data
    new_movie_data = Movie(
        title=movie_info.get('title', title),
        director=movie_info.get('director', request.form.get('director')),
        release_year=movie_info.get('release_year', year),
        rating=movie_info.get('rating', rating),
        poster=movie_info.get('poster', request.form.get('poster')),
        genre=movie_info.get('genre', request.form.get('genre')),
        countries=movie_info.get('countries', request.form.get('countries')),
        description=movie_info.get('description', request.form.get('description')),
        imdb_id=movie_info.get('imdb_id', request.form.get('imdb_id')),
        user_id=user_id
    )
    
    data_manager.add_movie(new_movie_data)
    return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get('title')
    data_manager.update_movie(movie_id, new_title)
    return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>')
def movie_details(user_id, movie_id):
    movie = db.session.get(Movie, movie_id)
    if not movie:
        return render_template('404.html'), 404
    return render_template('movie_details.html', movie=movie, user_id=user_id)


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('name')
    if name:
        data_manager.create_user(name)
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/test-500')
def test_500():
    raise Exception("Testing 500 error page")


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback() # Reset DB session on error
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run('localhost', 5001, debug=True)