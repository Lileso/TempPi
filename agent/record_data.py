from datetime import datetime
import time
#import Adafruit_DHT as Sensor
import threading
import yaml
import pathlib
import requests
p = pathlib.Path('config/agent.yaml')
config = yaml.safe_load(p.open())
agent_config = config['agent']
server_config = config['agent']

sensor_args = {	'11': Sensor.DHT11, '22': Sensor.DHT22, '2302': Sensor.AM2302}

'''def add_parser_options(parser):
    parser.add_option('-t', action="store", type="int", default=15, help="time interval in minutes to request readout from sensor [default: %default]")
    parser.add_option('--pin', dest="pin", action="store", type="int", default=4, help="data pin connected to sensor [default: %default]")
    parser.add_option('-s', action="store", type="str", default='11', help="number of DHT sensor in use (supported: 11, 22, 2302) [default: %default]")
    return parser
'''

class SensorDatabase(threading.Thread):
    def __init__(self, pin, sensor_number, minutes_interval):
        self.pin = pin
        self.sensor_number = sensor_number
        self.minutes_interval = minutes_interval
        threading.Thread.__init__(self)

    def record_to_database(self, data):
        humidity, temperature, datetime = data
        json_data={}
        json_data['humidity']= humidity
        json_data['temperature']= temperature
        json_data['datetime']=datetime
        requests.post(url=f"http://{server_config['server_url']}:{server_config['server_port']}",json=json_data)

    def run(self):
        while True:
            humidity, temperature = Sensor.read_retry(self.sensor_number, self.pin)
            data = humidity, temperature, datetime.now()
            self.record_to_database(data)
            one_minute = 60
            sleep_time = self.minutes_interval * one_minute
            time.sleep(sleep_time)

if __name__ == "__main__":
    sd = SensorDatabase(agent_config['pin'], agent_config["sensor"], agent_config['time'])
    sd.run()