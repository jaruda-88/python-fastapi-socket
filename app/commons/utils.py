from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Union, Any
from commons.const import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
    ALGORITH
)

# pip install "python-jose[cryptography]" "passlib[bcrypt]" python-multipart
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    '''
    get hased pwd
    :param password: origin pwd
    :return: hash pwd
    '''

    return password_context.hash(password)


def verify_password(password: str, hash_pwd: str) -> bool:
    '''
    password 검증
    :param password: origin pwd
    :return: bool
    '''

    return password_context.verify(password, hash_pwd)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    '''
    get token
    :param subject:
    :param expires_delta:
    :return: jwt token
    ''' 

    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {"exp": expires_delta, "sub": str(subject)}
    encoded = jwt.encode(payload, JWT_SECRET_KEY, ALGORITH)

    return encoded

