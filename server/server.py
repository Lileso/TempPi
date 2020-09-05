from flask import Flask, render_template,jsonify, Blueprint
from blueprint import api

def add_parser_options(parser):
    parser.add_option('--port', dest="port", action="store", type="int", default=80, help="port [default: %default]")
    parser.add_option('--host', dest="host", action="store", type="str", default='0.0.0.0', help="host [default: %default]")
    parser.add_option('-n', action="store", type="int", default=100, help="max limit of rows avilable by /data/ [default: %default]")
    return parser

app = Flask(__name__)
app.register_blueprint(api)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<agent_name>')
def graph(agent_name):
    return render_template('graph.html', agent_name=agent_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True) 