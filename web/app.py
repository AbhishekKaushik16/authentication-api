import logging

from flask import request, jsonify, make_response
from api.base.client import Client
from api.models.user import register_user, login_user, update_user, delete_user, email_confirmed
from api.utils.helpers import confirm_token
from web.config import env, app
from api.utils.logger import logger
from web.decoraters import check_token

if env.get("debug", "false").lower() == "true":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

client = Client(env)


@app.route("/accounts/register", methods=["POST"])
def signup():
    data = request.get_json()
    body, code = register_user(client, data)
    return make_response(jsonify(body)), code


@app.route("/accounts/login", methods=["POST"])
def login():
    data = request.get_json()
    body, code = login_user(client, data)
    return make_response(jsonify(body)), code


# TODO: an route for changing email, password
@app.route('/accounts/update', methods=['PUT'])
@check_token
def update():
    data = request.get_json()
    body, code = update_user(client, data)
    return make_response(jsonify(body)), code


# TODO: an route for resetting password through email
@app.route('/accounts/delete', methods=["DELETE"])
@check_token
def delete():
    data = request.get_json()
    body, code = delete_user(client, data)
    return make_response(jsonify(body)), code


@app.route('/confirm/<token>', methods=["GET"])
# @check_token
def confirm_email(token):
    email = confirm_token(token)
    body, code = email_confirmed(client, email)
    return make_response(jsonify(body)), code


@app.route("/<resource_name>/<_id>", methods=["GET"])
@check_token
def get_user(resource_name, _id):
    try:
        body = client.search_by_id(
            resource=resource_name,
            _id=_id,
        )
        code = 200
    except Exception as exc:
        body = str(exc)
        code = 400
        logger.error(exc, exc_info=True)
    return make_response(jsonify(body), code)


@app.route("/<resource_name>", methods=["POST"])
@check_token
def add_user(resource_name):
    data = request.get_json()
    body = client.insert_data(resource_name, data)
    if body is False:
        return jsonify({"message": "Insertion Failed"})
    else:
        return jsonify({"message": "Successfully Inserted", "token": body["token"]})


@app.route('/<resource_name>', methods=['PUT'])
@check_token
def update_resource(resource_name):
    data = request.get_json()
    body = client.update_data(resource_name, data)
    if body:
        return jsonify({"message": "Resource Updated."})
    else:
        return jsonify({"message": "Updating Failed."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
