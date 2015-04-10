import datetime


__author__ = 'elhe'


class FoodDiaryEntry(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.date_time = kwargs.get('date_time', datetime.datetime.now())
        self.name = kwargs.get('name')
        self.weight = kwargs.get('weight', 0)
        self.bread_unit = kwargs.get('bread_unit', 0)
        self.note = kwargs.get('note', None)