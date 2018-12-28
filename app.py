# --------------------------------- Import Statements ------------------------------

from class_recommendation import Recommendation, Utils
from class_recommendation import Utils
import jsonpickle

from flask import Flask
from flask_restful import Api, Resource

# --------------------------------- Global Stuff ---------------------------------

app = Flask(__name__)
api = Api(app)

global recommender, utils

recommender = Recommendation()
utils = Utils()

# updating the movie-rating-matrix
recommender.update_movie_rating(4.0)

# ------------------------------------ Resources --------------------------------

class MovieList(Resource):

    def get(self):
        top_charts = []
        for id in recommender.top_n(10):
            print(id)
            top_charts.append({
                "movieId": id,
                "title": utils.get_movie_details(id)
            })
        return top_charts

class UserRecommendation(Resource):

    def get(self, userId, k = 10):
        top_n = []
        for id in recommender.top_recommendation(userId, k):
            print(id)
            top_n.append({
                "movieId": id,
                "title": utils.get_movie_details(id)
            })
        return top_n

# ---------------------------------- Running the server ---------------------------

api.add_resource(MovieList, '/top-charts')
api.add_resource(UserRecommendation, '/user/<int:userId>')

app.run(port=5000)