import unittest

from application.managers import food_diary_manager
from application.models.food_diary_entry import FoodDiaryEntry

from testfixtures import compare


__author__ = 'elhe'


class FoodDiaryTest(unittest.TestCase):
    def setUp(self):
        food_diary_manager.truncate()

    def test_save_diary(self):
        entry = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry)

        actual = food_diary_manager.find(entry)
        compare(actual['name'], entry.name)

    def test_all_entries(self):
        entry1 = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry1)
        entry2 = FoodDiaryEntry(name='Two', note='note two')
        food_diary_manager.save(entry2)

        actual = list(food_diary_manager.find_all())
        compare(2, len(actual))
        compare(entry1.name, actual[0]['name'])
        compare(entry2.name, actual[1]['name'])

    def test_edit_entry(self):
        entry = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry)

        entry.name = 'new name'
        food_diary_manager.update(entry)
        actual = food_diary_manager.find(entry)
        compare(entry.name, actual['name'])

    def test_delete_entry(self):
        entry = FoodDiaryEntry(name='One', note='note')
        food_diary_manager.save(entry)

        food_diary_manager.delete(entry.id)
        actual = list(food_diary_manager.find_all())
        assert not actual

    def test_delete_nonexistent_entry(self):
        food_diary_manager.delete(-1)
        actual = list(food_diary_manager.find_all())
        assert not actual

    def test_save_default_diary(self):
        entry = FoodDiaryEntry()
        food_diary_manager.save(entry)

        actual = food_diary_manager.find(entry)
        compare(actual['name'], entry.name)