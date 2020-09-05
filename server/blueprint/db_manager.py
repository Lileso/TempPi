from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Date
import yaml
import os
import datetime
import pathlib

p = pathlib.Path('config/server.yaml')
config = yaml.safe_load(p.open())
db_config = config['database']
class database:
    def __init__(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        self.engine = create_engine('sqlite:///'+script_path+'/dht_database.db')
        self.metadata = MetaData(bind=self.engine)
        self.metadata.create_all()
        self.metadata.reflect(bind=self.engine)

    def create_agent(self, agent_name):
        if not self.engine.dialect.has_table(self.engine, agent_name):
            agent_table = Table(agent_name, self.metadata, Column('id', Integer, primary_key=True, autoincrement=True), Column('humidity', Integer), Column('temperature',Integer), Column('date_time', Date))
            agent_table.create(bind=self.engine)
            self.metadata.reflect(bind=self.engine)

    def add_record(self, agent_name, humidity, temperature, date_time):
        agent_table = self.metadata.tables.get(agent_name)
        if agent_table is None:
            self.create_agent(agent_name)
            agent_table = self.metadata.tables.get(agent_name)
        add_data = agent_table.insert().values(humidity=humidity, temperature=temperature, date_time=date_time)
        self.engine.execute(add_data)

    def query_table(self, agent_name):
        agent_table = self.metadata.tables.get(agent_name)
        if agent_table is not None:
            search = agent_table.select().order_by(agent_table.c.id.desc()).limit(db_config['record_limit'])
            results = self.engine.execute(search).fetchall()
            humidity_list = [round(i[1],1) for i in results]
            temperature_list = [round(i[2],1) for i in results]
            date_list = [i[3] for i in results]
            temperature_trace = dict(x=date_list, y=temperature_list, name='Temperature (C)', line=dict(width=7, color= "red"))
            humidity_trace = dict(x=date_list, y=humidity_list, name='Humidity (%)', line=dict(width=7, color= "blue"))
            data= [humidity_trace,temperature_trace]
            current_temp = [temperature_list[0]]
            return {"Success":True, "data":data, "current_temp":current_temp}
        return{"Success": False}
    
    def remove_agent(self, agent_name):
        agent_table = self.metadata.tables.get(agent_name)
        if agent_table is not None:
            agent_table.drop(self.engine)

if __name__ == "__main__":
    db=database()
    db.add_record(agent_name="Test_agent", humidity=1, temperature=2, date_time=datetime.datetime.now())
    results = db.query_table("Test_agent")
    print(results)
    print("\nRunning Test for if nothing in DB")
    db.create_agent("Test_agent")
    print(db.query_table("Test_agent2"))
    print("\nRunning Test for dropping table")
    db.remove_agent("Test_agent")
    print("\nRunning Test for dropping a table that doesn't exist")
    db.remove_agent("Test_agent2")