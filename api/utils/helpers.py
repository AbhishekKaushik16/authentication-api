import datetime
from ..models.base import base_object
from sqlalchemy import inspect


def get_class_by_tablename(resource_name):
    base_class = [
        c
        for c in base_object._decl_class_registry.values()
        if hasattr(c, "__tablename__") and c.__tablename__ == resource_name
    ][0]
    return base_class


def get_all_attr(obj):
    result_dict = {}
    for attr in inspect(obj).mapper.column_attrs:
        model_field = attr.key
        db_field = attr._orig_columns[0].key
        value = getattr(obj, model_field)
        result_dict[db_field] = value
    return result_dict

def get_current_time():
    return datetime.datetime.utcnow()