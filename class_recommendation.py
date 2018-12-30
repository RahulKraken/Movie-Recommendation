# collaborative filtering recommendation engine for the movie recommender system

# importing important libraries
import numpy as np
import pandas as pd
# imprting pairwise_distances from sklearn.metrics.pairwise to find the cosine
# similarity between entities
from sklearn.metrics.pairwise import pairwise_distances

# class contains methods to return responses from the recommender system
class Recommendation:

    def __init__(self):
        # reading the dataset
        self.ratings = pd.read_csv('movie-ml-latest-small/ratings.csv')
        self.movies = pd.read_csv('movie-ml-latest-small/movies_cleaned.csv')

        # removing redundant row from movies dataframe
        self.movies = self.movies.iloc[:, 1:]


    def create_similarity_matrices(self):
        # importing the user-item-rating matrix
        self.user_movie_rating = pd.read_csv('movie-ml-latest-small/user_movie_rating.csv')

        # matrix for similarity determination
        # self.user_movie_matrix = self.user_movie_rating.iloc[:, 1:]

        # finding the similarity between users and items
        self.user_similarity = pairwise_distances(self.user_movie_rating.iloc[:, 1:], metric = 'cosine')
        self.item_similarity = pairwise_distances(self.user_movie_rating.iloc[:, 1:].T, metric = 'cosine')

        # proper indexing of the columns of similarity matrices
        self.user_similarity = pd.DataFrame(self.user_similarity, columns = self.user_movie_rating['userId'], index = self.user_movie_rating['userId'])
        self.item_similarity = pd.DataFrame(self.item_similarity, columns = self.movies['movieId'], index = self.movies['movieId'])

    
    # predict rating for a particular movie by a particular user using user-user collaborative filtering or 
    # item-item collaborative filtering
    def predict_rating(self, userId, movieId, type = 'user'):
        
        global sum_rating_similarity, sum_similarity, temp
        
        temp = []
        sum_rating_similarity = 0
        sum_similarity = 0
        
        if type == 'user':
            temp = self.ratings[self.ratings.movieId == movieId]
            
            for item in temp.itertuples():
                sum_rating_similarity = sum_rating_similarity + (self.user_similarity.at[userId, item[1]] * item[3])
                
                sum_similarity = sum_similarity + self.user_similarity.at[userId, item[1]]
            
            return (sum_rating_similarity / sum_similarity) if sum_similarity != 0 else 0
        
        elif type == 'item':
            temp = self.ratings[self.ratings.userId == userId]
            
            for item in temp.itertuples():
                sum_rating_similarity = sum_rating_similarity + (self.item_similarity.at[movieId, item[2]] * item[3])
                
                sum_similarity = sum_similarity + self.item_similarity.at[movieId, item[2]]
            
            return (sum_rating_similarity / sum_similarity) if sum_similarity != 0 else 0
        
        else:
            return 0
    
    # create a dateframe to store all the prediction
    def create_predictions_df(self):
        self.user_movie_prediction = pd.DataFrame(0.0, columns = self.movies['movieId'], index = np.arange(610))
        self.user_movie_prediction['userId'] = self.ratings['userId'].unique()

    # populate user_movie_prediction with the updated predictions values for all users    
    def update_predictions(self, userId):
        for movie in self.movies['movieId']:
            self.user_movie_prediction.at[userId - 1, movie] = (self.predict_rating(userId, movie, type = 'item') + self.predict_rating(userId, movie)) / 2
            # print(self.user_movie_prediction.at[userId - 1, movie])

    # return k number of best recommendations for given userId
    def top_recommendation(self, userId, k = 10):
        self.create_similarity_matrices()
        self.create_predictions_df()
        self.update_predictions(userId)
        movie_list = []
        top_n = self.user_movie_prediction.iloc[userId - 1, :].sort_values(ascending = False).head(k).tolist()
        print(top_n)
        for col in self.movies['movieId']:
            if self.user_movie_prediction.iloc[userId - 1][col] in top_n:
                movie_list.append(col)
        return movie_list

    # ------------------------- Top Charts -------------------------------

    # using weighted rating method used by imdb to find the top charts

    # populating movie_rating
    def update_movie_rating(self, min_count):
        
        # matrix containing movieId and it's average rating and count
        self.movie_rating = pd.DataFrame(0.0, columns = ['movieId', 'mean_rating', 'count', 'score'], index = self.movies['movieId'])
        global movie_rating
        mean_rating = 0
        count = 0
        
        average_rating_count = self.ratings.shape[0] / self.movies.shape[0]
        
        # populate the movieId mean_rating count and score one by one for each movie
        for movie in self.movies.itertuples():
            
            mean_rating = self.ratings[self.ratings.movieId == movie[1]].mean()['rating']
            count = self.ratings[self.ratings.movieId == movie[1]].count()['rating']
            
            # populate 'movieId'
            self.movie_rating.at[movie[1], 'movieId'] = movie[1]
            print(movie[1])
            
            # fill mean_rating
            self.movie_rating.at[movie[1], 'mean_rating'] = mean_rating
            
            # fill count
            self.movie_rating.at[movie[1], 'count'] = count
            
            # fill score
            self.movie_rating.at[movie[1], 'score'] = ((count / (count + min_count)) * mean_rating) / ((min_count / (count + min_count)) * average_rating_count)
            print(self.movie_rating.at[movie[1], 'score'])

    # return top n movies overall
    def top_n(self, n = 25, min_rating = 4.0):
        self.update_movie_rating(min_rating)
        return self.movie_rating.sort_values('score', ascending = False)['movieId'].head(n).tolist()

# -------------------------------- Utilities --------------------------------

class Utils:

    def __init__(self):
        # reading the dataset
        self.ratings = pd.read_csv('movie-ml-latest-small/ratings.csv')
        self.movies = pd.read_csv('movie-ml-latest-small/movies_cleaned.csv')

    def get_movie_details(self, movieId):
        return self.movies.at[self.movies.index[self.movies['movieId'] == movieId].tolist()[0], 'title']
