from flask import Flask, render_template, request
from models import UserPreference
from recommendation_engines import RecommendationEngine
from contents import content

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['preferences']
    user_preferences = UserPreference(user_input)

    recommendation_engine = RecommendationEngine(content)
    recommendations = recommendation_engine.recommend(user_preferences)

    return render_template('recommendations.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug = True, port = 8001)