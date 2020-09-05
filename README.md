# TempPi
A small project for centralising data from temperature and humidity sensors 
There is a web server and an agent. (They each have their own requirements)

## Agent

The agent is what takes the sensor readings and sends it to the server

The following DHT sensors are supported: 11, 22, 2302

the script depending on the config in `config/agent.yaml` the script will run this often and send data to the server.

to change the name given to the agent please edit the `config/agent.yaml` file or run the setup.py and restart the service

## Server

The Server collects data sent to it from any agent. It will automatically add that agent to the agent table which lets you pick which graph you want to view. 

There is an API:

### endpoints 

#### Add Record

POST `/api/<agent_name>/send_data`

This endpoint will take the agent_name and create the agent on the backend. No prior setup required!

```json
{
    "humidity":54,
    "temperature":19,
    "date_time":"2020-09-05 17:47:52" 
}
```
If you don't send this then you'll receive:
```json
{
    "exception_code": 422, 
    "exception_message": "Data missing from sent json. Data must include: temperature, humidity, data_time", 
    "success": false}
```

if all goes well you should receive:
```json
{
    "exception_code": 201, 
    "exception_message": "Added Data to Database", 
    "success": true
}
```

#### Get Data

GET `/api/<agent_name>/get_data`

This will return a JSON string that contains the last 100 (by default but can be changed in the config) records

```json
{
  "Success": true,
  "current_temp": [
    19
  ],
  "data": [
    {
      "line": {
        "color": "blue",
        "width": 7
      },
      "name": "Humidity (%)",
      "x": [
        "Sat, 05 Sep 2020 00:00:00 GMT"
      ],
      "y": [
        54
      ]
    },
    {
      "line": {
        "color": "red",
        "width": 7
      },
      "name": "Temperature (C)",
      "x": [
        "Sat, 05 Sep 2020 00:00:00 GMT"
      ],
      "y": [
        19
      ]
    }
  ]
}
```
#### Delete Agent

DELETE `/api/<agent_name>/delete_agent`

This endpoint deletes the agent and all its data with it. Be careful when hitting it.

when its done you'll receive the following JSON

```json
{
  "exception_code": 201,
  "exception_message": "Agent deleted from server",
  "success": true
}
```