import sqlite3

# CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)
# INSERT INTO users VALUES(NULL, ?, ?)

class Database():

    def __init__(self):
        pass
    
    @staticmethod
    def create_table_users():
        create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(create_table)
        connection.commit()
        connection.close()
    
    @staticmethod
    def add_user(username, password):
        add_user = "INSERT INTO users VALUES(NULL, ?, ?)"
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(add_user, (username, password))
        connection.commit()
        connection.close()

    @staticmethod
    def create_predictions_table():
        create_table = "CREATE TABLE IF NOT EXISTS predictions (userId INTEGER PRIMARY KEY, "
        for i in range(25):
            create_table = create_table + "movie" + str(i) + " INTEGER NOT NULL, "
        create_table = create_table[:-2] + ")"
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(create_table)
        connection.commit()
        connection.close()

    @staticmethod
    def add_user_prediction(userId, movies):
        add_prediction = "INSERT INTO predictions VALUES (" + str(userId) + ", "
        for movie in movies:
            add_prediction = add_prediction + str(movie) + ", "
        add_prediction = add_prediction[:-2] + ")"
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(add_prediction)
        connection.commit()
        connection.close()

    @staticmethod
    def get_user_prediction(userId):
        get_movies = "SELECT * FROM predictions WHERE userId = " + str(userId);
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(get_movies)
        row = cursor.fetchone()
        print(row)
        return row
