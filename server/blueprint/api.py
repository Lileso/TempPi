from flask import Blueprint, jsonify, request
from db_manager import database
import datetime

api = Blueprint('api', __name__)
db = database()

@api.route('/api/<agent_name>/get_data')
def get_data(agent_name):
    ''' This is an endpoint that the website can use to get and graph data.  
    agent_name: This is a variable that is used to work out what agent is what in the DB file. Usually hostname of the agent.
    '''
    data = db.query_table(agent_name)
    return jsonify(data)

@api.route('/api/<agent_name>/send_data', method=["POST"])
def send_data(agent_name):
    ''' This is an endpoint that the agents use to sent their data. 
    agent_name: This is a variable that is used to work out what agent is what in the DB file. Usually hostname of the agent.

    Required JSON:
    temperature : Value of recorded temp
    humidity :  Value of recorded humidity
    date_time : date and time of the sensor reading
    '''
    if not request.is_json:
        return jsonify({"exception_code": 400, "exception_message": "Invalid type, Please send JSON", "success": False}), 400
    sent_json = request.get_json()
    if "temperature" not in sent_json or "humidity" not in sent_json or "date_time" not in sent_json:
        return jsonify({"exception_code": 422, "exception_message": "Data missing from sent json. Data must include: temperature, humidity, data_time", "success": False}), 422
    db.add_record(agent_name=agent_name, humidity=sent_json['humidity'], temperature=sent_json['temperature'], date_time=sent_json['date_time'])
    return jsonify({"exception_code": 201, "exception_message": "Added Data to Database", "success": True}), 201

@api.route('/api/<agent_name>/delete_agent', method=['POST'])
def delete_data(agent_name):
    db.remove_agent(agent_name)
    return jsonify({"exception_code": 201, "exception_message": "Agent deleted from server", "success": True}), 201