# collaborative filtering recommendation engine for the movie recommender system

# import important libraries
import numpy as np
import pandas as pd

from multiprocessing.dummy import Pool as ThreadPool

# ------------------------------- Importing the dataset ---------------------------------

# reading the dataset
ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies_cleaned.csv')

# removing redundant row from movies dataframe
movies = movies.iloc[:, 1:]

# importing the user-item-rating matrix
user_movie_rating = pd.read_csv('user_movie_rating.csv')

# removing the useless columns
# user_movie_rating = user_movie_rating.iloc[:, 1:]

# matrix for similarity determination
user_movie_matrix = user_movie_rating.iloc[:, 1:]


# ------------------------- Building the Recommendation Engine --------------------------


# -------------------------------- Collaborative Model-----------------------------------

# finding the similarity between users and items

# importing pairwise_distances from skelarn.metrics.pairwise to find the 
# cosine similarity between entities
from sklearn.metrics.pairwise import pairwise_distances

user_similarity = pairwise_distances(user_movie_matrix, metric = 'cosine')
item_similarity = pairwise_distances(user_movie_matrix.T, metric = 'cosine')

# proper and index and column name to similarity matrices
user_similarity = pd.DataFrame(user_similarity, columns = user_movie_rating['userId'], index = user_movie_rating['userId'])
item_similarity = pd.DataFrame(item_similarity, columns = movies['movieId'], index = movies['movieId'])

temp = []
sum_rating_similarity = 0
sum_similarity = 0

# prediction function to predict the result
# prediction made on the basis of user-user or item-item collaborative filtering
def predict_rating(userId, movieId, user_movie_rating, similarity, type = 'user'):
    global sum_rating_similarity, sum_similarity, temp
    
    sum_rating_similarity = 0
    sum_similarity = 0
    
    if type == 'user':
        # TODO(1): get the users who rated a movie
        temp = ratings[ratings.movieId == movieId]
        # similar_user = -np.sort(-similarity[0])
        
        for item in temp.itertuples():
            # TODO(2): loop through found users and find the sum of thier ratings times their similarity
            sum_rating_similarity = sum_rating_similarity + (similarity.at[userId, item[1]] * item[3])
            
            # TODO(3): find the sum of their similarity too    
            sum_similarity = sum_similarity + similarity.at[userId, item[1]]
        
        # TODO(4): after the loop ends divide them to get the predicted rating
        return (sum_rating_similarity / sum_similarity) if sum_rating_similarity != 0 and sum_similarity != 0 else 0
    
    elif type == 'item':
        # TODO(1): get the movies rated by the user
        temp = ratings[ratings.userId == userId]
        
        for item in temp.itertuples():
            # TODO(2): loop through found movies and find sum of their ratings times their similarity
            sum_rating_similarity = sum_rating_similarity + (similarity.at[movieId, item[2]] * item[3])
            
            # TODO(3): find the sum of their similarities
            sum_similarity = sum_similarity + similarity.at[movieId, item[2]]
        
        # TODO(4): return the item-item collaborative filtering rating
        return (sum_rating_similarity / sum_similarity) if sum_rating_similarity != 0 and sum_similarity != 0 else 0
    
    else:
        return 0


# a dataframe to store all the prediction
user_movie_prediction = pd.DataFrame(0.0, columns = movies['movieId'], index = np.arange(610))
user_movie_prediction['userId'] = user_movie_rating['userId']

# populate user_movie_prediction with the updated predictions values for all users    
def update_predictions(userId):
    # for row in range(user_movie_prediction.shape[0]):
    for movie in movies['movieId']:
        print("movieId - ", movie, " - userId - ", userId)
        user_movie_prediction.at[userId - 1, movie] = (predict_rating(userId, movie, user_movie_rating, user_similarity) + predict_rating(userId, movie, user_movie_rating, item_similarity, type = 'item')) / 2
        # print(user_movie_prediction.at[row, movie])

"""
pool = ThreadPool(120)
results = pool.map(update_predictions, user_movie_prediction['userId'].tolist())
pool.close()
pool.join()
"""

# return k number of best recommendations for given userId
def top_recommendation(userId, k = 10):
    update_predictions(userId)
    movie_list = []
    top5 = user_movie_prediction.iloc[userId - 1, :].sort_values(ascending = False).head(k).tolist()
    print(top5)
    for col in user_movie_prediction.columns:
        if user_movie_prediction.iloc[userId - 1][col] in top5:
            print(col)
            movie_list.append(col)
    return movie_list

# ----------------------------------- Top Charts ----------------------------------------

# using weighted rating method used by imdb to find the top charts

# matrix containing movieId and it's average rating and count
movie_rating = pd.DataFrame(0.0, columns = ['movieId', 'mean_rating', 'count', 'score'], index = movies['movieId'])

# populating movie_rating
def update_movie_rating(min_count):
    global movie_rating
    mean_rating = 0
    count = 0
    
    average_rating_count = ratings.shape[0] / movies.shape[0]
    
    # populate the movieId mean_rating count and score one by one for each movie
    for movie in movies.itertuples():
        
        mean_rating = ratings[ratings.movieId == movie[1]].mean()['rating']
        count = ratings[ratings.movieId == movie[1]].count()['rating']
        
        # populate 'movieId'
        movie_rating.at[movie[1], 'movieId'] = movie[1]
        print(movie[1])
        
        # fill mean_rating
        movie_rating.at[movie[1], 'mean_rating'] = mean_rating
        
        # fill count
        movie_rating.at[movie[1], 'count'] = count
        
        # fill score
        movie_rating.at[movie[1], 'score'] = ((count / (count + min_count)) * mean_rating) / ((min_count / (count + min_count)) * average_rating_count)
        print(movie_rating.at[movie[1], 'score'])


# return top n movies overall
def top_n(n):
    return movie_rating.sort_values('score', ascending = False)['movieId'].head(n).tolist()


# --------------------------------------------- Utilty Methods --------------------------------------

def get_movie_name(movieId):
    return movies[movies.movieId == movieId]["title"]













