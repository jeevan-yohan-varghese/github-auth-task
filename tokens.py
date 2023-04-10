
from datetime import datetime, timedelta
from fastapi import HTTPException
import jwt
import os
from dotenv import load_dotenv

from fastapi.security import OAuth2PasswordBearer

load_dotenv(".env") 
SECRET_KEY=os.environ["SECRET_KEY"]
algorithm='HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/github_login")
def create_access_token(data: dict, expires_delta: timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=algorithm)
    return encoded_jwt


def decode_token(token: str):
    details={}
    try:
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        
        github_access = payload.get("gh_access")
        details['gh_access']=github_access
        details['username']=payload.get("username")
        if github_access is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    return details