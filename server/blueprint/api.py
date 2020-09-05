from flask import Blueprint, jsonify

api = Blueprint('api', __name__)

api.route('/api/<agent_name>/get_data')
def get_data():
    return "Data"

api.route('/api/<agent_name>/send_data')
def send_data():
    return "Done!"