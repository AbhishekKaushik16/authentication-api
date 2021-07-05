def update_object_from_dict(obj, data: dict):
    for k, v in data.items():
        setattr(obj, k, v)
    return obj
