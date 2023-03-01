from os import getenv, environ

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30   # 30분
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7     # 7일
ALGORITH: str = "HS256"
JWT_SECRET_KEY: str = environ.get('JWT_SECRET_KEY', '1q2w3e4r5t')
JWT_REFRESH_SECRET_KEY: str = getenv('JWT_REFRESH_SECRET_KEY')