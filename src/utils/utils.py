from bson import ObjectId
from datetime import datetime

def serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.date().isoformat()
    else:
        raise TypeError("Type %s not serializable" % type(obj))