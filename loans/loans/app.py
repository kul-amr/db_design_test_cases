from flask import Flask
from backend import *
from . import config as config


def create_app(config):
    loans_app = Flask(__name__)

    loans_app.config.from_object(config)

    db.init_app(loans_app)
    db.create_all(app = loans_app)
    return loans_app

loans_app = create_app(config=config)

@loans_app.route('/')
def home():
    return "starting app!"

if __name__ == '__main__':
    loans_app.run()



