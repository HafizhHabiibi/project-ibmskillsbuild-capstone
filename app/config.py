from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123'
    SESSION_TYPE = 'filesystem'