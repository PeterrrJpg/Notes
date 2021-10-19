from json import dumps
from flask import Flask, request

APP = Flask(__name__)

names = {
    'name' : []
}

@APP.route('/names/add', methods=['POST'])
def add_new_name():
    request_data = request.get_json()
    new_name = request_data['name']
    names['name'].append(new_name)
    return dumps({})

@APP.route('/names', methods=['GET'])
def get_names():
    return dumps(names)

@APP.route('/names/remove', methods=['DELETE'])
def remove_name():
    request_data = request.get_json()
    target_name = request_data['name']
    names['name'].remove(target_name)
    return dumps({})

@APP.route('/names/clear', methods=['DELETE'])
def clear_names():
    names['name'].clear()
    return dumps({})

if __name__ == "__main__":
    APP.run(debug = True, port = 5000)
