# Data model for Movie
class Movie:

    def __init__(self, name, movieId):
        self.name = name
        self.movieId = movieId
    
    def getMovie(self):
        return {
            "movieId": self.movieId,
            "name": self.name
        }