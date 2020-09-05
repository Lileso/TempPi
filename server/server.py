from flask import Flask, render_template,jsonify, Blueprint
from blueprint.api import api
from blueprint.db_manager import database
import pathlib
import yaml

db = database()

p = pathlib.Path('config/server.yaml')
with p.open(mode='r') as f:
    config = yaml.safe_load(f)
api_config = config['webserver']

app = Flask(__name__)
app.register_blueprint(api)

@app.route('/')
def index():
    return render_template('index.html', table_list=db.table_list())

@app.route('/<agent_name>')
def graph(agent_name):
    return render_template('graph.html', agent_name=agent_name)

if __name__ == '__main__':
    app.run(host=api_config['host'], port=api_config['port'], debug=api_config['debug']) 