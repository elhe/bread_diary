from flask import Flask

__author__ = 'elhe'

application = Flask(__name__)
from application import service
from application.service import food_diary_service