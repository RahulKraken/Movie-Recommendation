import sqlite3
from flask_restful import Resource, reqparse

class Registeration(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type = str,
        required = True,
        help = 'This field can not be empty'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'This field can not be empty'
    )

    def post(self):

        data = Registeration.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        insert_query = "INSERT INTO users VALUES(NULL, ?, ?)"

        cursor.execute(insert_query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"message":"User registered successfully"}, 201
    
        
        