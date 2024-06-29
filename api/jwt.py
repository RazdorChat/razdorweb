import jwt

def verifyToken(key : str, token : str):
    try:
        decoded_token = jwt.decode(token, key, algorithms=['HS256'])
        # Token is valid
        return True
    except jwt.exceptions.InvalidTokenError:
        # Token is invalid
        return False
    
def createToken(key : str, payload : str):
    token = jwt.encode(payload, key, algorithm="HS256")
    return token

def extractToken(key : str, token : str):
    if verifyToken(key, token):
        Dtoken = jwt.decode(token, key, algorithms=["HS256"])
        return Dtoken
    else:
        return "Invalid"
