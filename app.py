# --------------------------------- Import Statements ------------------------------

from class_recommendation import Recommendation, Utils
from security import authenticate, identity

from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required

from database import Database

from registeration import Registeration

# --------------------------------- Global Stuff ---------------------------------

app = Flask(__name__)
api = Api(app)

# security thing
app.secret_key = 'kajdkfalJDHJjshdkayeiupqnb'

jwt = JWT(app, authenticate, identity)                      # /auth end-point created by this object

global recommender, utils

recommender = Recommendation()
utils = Utils()

# updating the movie-rating-matrix
recommender.update_movie_rating(4.0)

# creating the needed dataframes
recommender.create_similarity_matrices()
recommender.create_predictions_df()

Database.create_table_users()
Database.create_predictions_table()

# ------------------------------------ Resources --------------------------------

class HelloWorld(Resource):

    def get(self):
        return "Hello World from the server"

class MovieList(Resource):

    @jwt_required()
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

    @jwt_required()
    def get(self, userId, k = 25):
        top_n = []
        movie_list = Database.get_user_prediction(userId)
        if movie_list:
            print(movie_list)
        else:
            movie_list = recommender.top_recommendation(userId, k)
            Database.add_user_prediction(userId, movie_list[:25])
        for id in movie_list:
            print(id)
            top_n.append({
                "movieId": id,
                "title": utils.get_movie_details(id)
            })
        return top_n[:25]

# ---------------------------------- Running the server ---------------------------

api.add_resource(HelloWorld, '/')
api.add_resource(MovieList, '/top-charts')
api.add_resource(UserRecommendation, '/user/<int:userId>')
api.add_resource(Registeration, '/register')

app.run(port=5000)