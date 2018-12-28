# Movie Recommendation System (Completely from me)

# import important libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# importing the dataframes
df_movies = pd.read_csv('movies_cleaned.csv')
df_ratings = pd.read_csv('ratings.csv')

# visualizing the dataframes
df_movies.head(100)
df_ratings.head(100)

# we need to make a matrix with the users as the index and the movies as the columns and the values with the
# ratings given by the users and 0 where there's no value.
# we need to predict the value that will go at the empty places for all users

# all movies rated by users grouped by their useId
movies_rated = df_ratings.groupby('userId')['movieId'].apply(list)
userIds = movies_rated.index.values

# this is the dataframe we'll use to store our movie ratings
user_movie_rating = pd.DataFrame()

movieIds = []
for i in range(df_movies.shape[0]):
    print(df_movies.at[i, 'movieId'])
    movieIds.append(df_movies.at[i, 'movieId'])

j = 0
movieIds.sort()
ratings_matrix = pd.DataFrame(0, index = range(610), columns = movieIds)

user_movie_rating = user_movie_rating.add(ratings_matrix, axis = 1)

# adding the userIds
for i in range(userIds.shape[0]):
    user_movie_rating.at[i, 'userId'] = str(userIds[i])

movieIds = []
last_user = 0
last_user_pos = 0

# movieId = 47 and userId = 1
def getRating(userId, movieId, k):
    for i in range(k, df_ratings.shape[0]):
        if df_ratings.at[i, 'userId'] == userId and df_ratings.at[i, 'movieId'] == movieId:
            print(userId, df_ratings.at[i, 'rating'])
            return df_ratings.at[i, 'rating'], k + 1
    return 0, k + 1

# making a list of all movie 
for userId in userIds:
    for movieId in movies_rated[userId]:
        user_movie_rating.at[userId - 1, movieId], j = getRating(userId, movieId, j)

user_movie_rating = user_movie_rating.fillna(0)
user_movie_rating.to_csv('user_movie_rating.csv', encoding = 'UTF-8')
