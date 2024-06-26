from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_top_100_movies():

    url = "https://imdb-top-100-movies.p.rapidapi.com/"

    headers = {
        "x-rapidapi-key": "5309fb426dmsh8fce2e17c08218bp1cc218jsne1698a9882d0",
        "x-rapidapi-host": "imdb-top-100-movies.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


@app.route('/')
def index():
    movies = get_top_100_movies()
    return render_template('home.html', movies = movies)

if __name__ == "__main__":
    app.run(debug = True, port = 8001)
