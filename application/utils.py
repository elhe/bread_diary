from datetime import datetime
import json

__author__ = 'elhe'


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.strftime('%b %d %Y %I:%M%p')
        return serial
    return obj


def object_json(obj):
    return json.dumps(object_dict(obj), default=json_serial)


def object_dict(obj):
    return dict(
        (name, getattr(obj, name)) for name in dir(obj) if
        (not name.startswith('__') and not callable(getattr(obj, name))))