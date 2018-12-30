from werkzeug.security import safe_str_cmp
from user import User

# authenticate method for authentication
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# identity method, unique to flask-jwt and takes a payload
def identity(payload):
    print('payload - ', payload)
    userid = payload['identity']
    return User.find_by_id(userid)
