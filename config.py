import os

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-fallback-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///members.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
