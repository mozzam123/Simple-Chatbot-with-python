import os
from datetime import timedelta
import urllib
import urllib.parse




class Config:
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://kannel:{enc_pasword}@localhost/Main'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'sarib'  # Change this!
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  

