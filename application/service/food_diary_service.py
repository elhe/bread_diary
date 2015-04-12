from datetime import datetime

from application import application
from application.managers import food_diary_manager
from application.models.food_diary_entry import FoodDiaryEntry
from application.urls import DIARY_ADD_URL, DIARY_UPDATE_URL, DIARY_DELETE_URL, DIARY_ALL_URL
from dateutil import parser
from flask import request
from flask.json import jsonify


__author__ = 'elhe'


@application.route(DIARY_ALL_URL, methods=['GET', ])
def entries():
    return jsonify(**{'entries': list(food_diary_manager.find_all())})


@application.route(DIARY_ADD_URL, methods=['POST', ])
def add():
    data = request.get_json()
    if data.get('date_time'):
        data['date_time'] = datetime.strptime(data['date_time'], '%b %d %Y %I:%M%p')
    entry = FoodDiaryEntry(**data)
    food_diary_manager.save(entry)
    return jsonify(dict(status='OK', id=entry.id))


@application.route(DIARY_UPDATE_URL, methods=['PUT', ])
def update():
    data = request.get_json()
    data['date_time'] = parser.parse(data['date_time'])
    entry = FoodDiaryEntry(**data)
    food_diary_manager.update(entry)
    return jsonify(dict(status='OK'))


@application.route(DIARY_DELETE_URL, methods=['DELETE', ])
def delete():
    data = request.get_json()
    food_diary_manager.delete(data['id'])
    return jsonify(dict(status='OK'))