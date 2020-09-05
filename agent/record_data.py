from datetime import datetime
import socket
import time
#import Adafruit_DHT as Sensor
import threading
import yaml
import pathlib
import requests
p = pathlib.Path('config/agent.yaml')
with p.open(mode='r') as f:
    config = yaml.safe_load(f)
agent_config = config['agent']
server_config = config['server_connection']

sensor_args = {	'11': Sensor.DHT11, '22': Sensor.DHT22, '2302': Sensor.AM2302}

class SensorDatabase(threading.Thread):
    def __init__(self, pin, sensor_number, minutes_interval):
        self.pin = pin
        self.sensor_number = sensor_number
        self.minutes_interval = minutes_interval
        threading.Thread.__init__(self)

    def record_to_database(self, data):
        humidity, temperature, datetime = data
        agent_name = agent_config['name']
        if agent_name == "Hostname":
            agent_name = socket.gethostname()
        json_data={}
        json_data['humidity']= humidity
        json_data['temperature']= temperature
        json_data['datetime']=datetime.strftime("%Y-%m-%d %H:%M:%S")
        requests.post(url=f"http://{server_config['server_url']}/api/{agent_name}/send_data:{server_config['server_port']}",json=json_data)

    def run(self):
        while True:
            humidity, temperature = Sensor.read_retry(self.sensor_number, self.pin)
            data = humidity, temperature, datetime.now()
            self.record_to_database(data)
            one_minute = 60
            sleep_time = self.minutes_interval * one_minute
            time.sleep(sleep_time)

if __name__ == "__main__":
    sd = SensorDatabase(agent_config['pin'], agent_config["sensor"], agent_config['time_in_minutes'])
    sd.run()