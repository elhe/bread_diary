from application.utils import object_dict

import dataset


__author__ = 'elhe'

table_name = 'food_diary'


def save(entry):
    with dataset.connect() as tx:
        _id = tx[table_name].insert(object_dict(entry))
        entry.id = _id


def update(entry):
    with dataset.connect() as tx:
        tx[table_name].upsert(object_dict(entry), ['id'])


def find(entry):
    return dataset.connect()[table_name].find_one(id=entry.id)


def delete(entry_id):
    with dataset.connect() as tx:
        tx[table_name].delete(id=entry_id)


def find_all(limit=10):
    return dataset.connect()[table_name].find(_limit=limit)


def truncate():
    with dataset.connect() as tx:
        tx[table_name].delete()
