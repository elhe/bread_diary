import json
import unittest

from dateutil import parser

from application import application

from application.managers import food_diary_manager
from application.models.food_diary_entry import FoodDiaryEntry
from application.urls import DIARY_ADD_URL, DIARY_UPDATE_URL, DIARY_DELETE_URL, DIARY_ALL_URL
from application.utils import object_json, object_dict
from testfixtures import compare


__author__ = 'elhe'


class TestFoodDiaryService(unittest.TestCase):
    def setUp(self):
        food_diary_manager.truncate()
        self.app = application.test_client()

    def test_add(self):
        entry = FoodDiaryEntry(name='One', note='note')
        response = self.app.post(DIARY_ADD_URL, headers={'content-type': 'application/json'},
                                 data=object_json(entry))
        response_json = json.loads(response.data)
        assert response_json['id']
        compare('OK', response_json['status'])

        entry.id = response_json['id']
        actual = food_diary_manager.find(entry)
        assert actual
        compare(entry.name, actual['name'])
        compare(entry.note, actual['note'])

    def test_edit(self):
        entry = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry)

        entry.name = 'New name'
        response = self.app.put(DIARY_UPDATE_URL, headers={'content-type': 'application/json'},
                                data=object_json(entry))
        response_json = json.loads(response.data)
        compare('OK', response_json['status'])

        actual = food_diary_manager.find(entry)
        assert actual
        compare(entry.name, actual['name'])
        compare(entry.note, actual['note'])

    def test_delete(self):
        entry = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry)

        response = self.app.delete(DIARY_DELETE_URL, headers={'content-type': 'application/json'},
                                   data=json.dumps(dict(id=entry.id)))
        response_json = json.loads(response.data)
        compare('OK', response_json['status'])

        actual = food_diary_manager.find(entry)
        assert not actual

    def test_all_entries(self):
        entry1 = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry1)
        entry2 = FoodDiaryEntry(name='Two', note='note')
        food_diary_manager.save(entry2)

        response = self.app.get(DIARY_ALL_URL)
        response_json = json.loads(response.data)
        
        for entry in response_json['entries']:
            entry['date_time'] = parser.parse(entry['date_time'])

        compare(object_dict(entry1), response_json['entries'][0])
        compare(object_dict(entry2), response_json['entries'][1])


