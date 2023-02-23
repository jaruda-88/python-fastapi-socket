from passlib.context import CryptContext
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    '''
    get hased pwd
    :param password: origin pwd
    :return: hash pwd
    '''

    return password_context.hash(password)


def verify_password(password: str) -> bool:
    '''
    password 검증
    :param password: origin pwd
    :return: bool
    '''

    return password_context.verify(password, get_hashed_password(password))

