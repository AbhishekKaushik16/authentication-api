import requests

def update_object_from_dict(obj, data: dict):
    for k, v in data.items():
        setattr(obj, k, v)
    return obj

def check_if_email_exists(email: str) -> str:
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params={'email': email})
    status = response.json()['status']

    if status == "valid":
        return 'valid'
    elif status == "invalid":
        return 'invalid'
    else:
        return 'unknown'
