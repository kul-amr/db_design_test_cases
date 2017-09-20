import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'loans.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True