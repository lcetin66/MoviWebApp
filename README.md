# MovieWeb-App 🎬

A modern, responsive movie collection management web application built with **Flask** and **SQLAlchemy**. It integrates with the **OMDB API** to automatically fetch movie details and features a clean, professional blue-themed UI.

## 🚀 Features

- **User Management**: Create multiple users to manage separate movie collections.
- **OMDB API Integration**: Automatically fetches Movie Title, Year, Director, Genre, Rating, and Poster from OMDB when adding a movie.
- **Responsive UI**: A clean, light-themed design with card-based layouts and smooth transitions.
- **Detailed Movie Views**: View complete information about each movie, including plot summaries and IMDb links.
- **Custom Error Pages**: Hand-crafted 404 (Not Found) and 500 (Internal Server Error) pages with cinematic themes.
- **Environment Safety**: Secure management of API keys using `.env`.

## 🛠️ Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLite, Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3 (Vanilla)
- **API**: OMDB API

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lcetin66/MoviWebApp.git
   cd MoviWebApp
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install flask flask-sqlalchemy requests python-dotenv
   ```

4. **Add your OMDB API Key**:
   Create a `.env` file in the root directory:
   ```env
   OMDB_API_KEY=your_key_here
   SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```
   Open `http://localhost:5001` in your browser.

## 📄 License

This project is open-sourced under the MIT License.
