import jwt
from datetime import datetime,timedelta
from decouple import config

jwt_secret=config('jwt_secret')
jwt_algos=config('jwt_algos')

class JWT_Builder:
    def __init__(self,payload,enc=None):
        self.payload=payload
        self.enc=enc
        self.now = datetime.now()
        self.key=jwt_secret
        self.algo=jwt_algos

    def concat(self,b):
        return {**self.payload,**b}

    def get_token(self):
        access_token_exp=datetime.timestamp(self.now+timedelta(hours=1))
        refresh_token_exp=datetime.timestamp(self.now+timedelta(hours=1.5))

        access_token=jwt.encode((self.concat(b={"exp":access_token_exp,"iat":(datetime.timestamp(self.now))})),self.key,algorithm=self.algo)
        resfresh_token=jwt.encode((self.concat(b={"exp":refresh_token_exp,"iat":(datetime.timestamp(self.now))})),self.key,algorithm=self.algo)
        data={
            "access_token":access_token,
            "refresh_token":resfresh_token
        }
        return data
    