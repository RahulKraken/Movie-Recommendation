import sqlite3
from flask_restful import Resource, reqparse
from database import Database

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
        Database.add_user(data['username'], data['password'])
        return {"message":"user registered successfully"}, 201
    
        
        