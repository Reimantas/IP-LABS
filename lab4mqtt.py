import sqlite3
import paho.mqtt.client as mqtt
import json

MQTT_Topic = "Home/BedRoom/#"
mqttBroker = "broker.hivemq.com"

# SQLite DB Name
DB_Name = "IoT.db"

# SQLite DB Table Schema
TableSchema = """
drop table if exists Temperature_Data;
create table Temperature_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Temperature text
);

drop table if exists Humidity_Data;
create table Humidity_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Humidity text
);

drop table if exists Pressure_Data;
create table Pressure_Data (
  id integer primary key autoincrement,
  SensorID text,
  Date_n_Time text,
  Pressure text
);
"""

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_Name)
        self.conn.execute('pragma collaboratively_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()
        
    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()

def build_db(TableSchema):
    # Connect or Create DB File
    conn = sqlite3.connect(DB_Name)
    curs = conn.cursor()

    # Create Tables
    sqlite3.complete_statement(TableSchema)
    curs.executescript(TableSchema)

    # Close DB
    curs.close()
    conn.close()

def Temp_Data_Handler(jsonData):
    # Parse Data 
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Temperature = json_Dict['Temperature']
    
    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Temperature_Data (SensorID, Date_n_Time, Temperature) values (?,?,?)", [SensorID, Data_and_Time, Temperature])
    del dbObj
    print("Inserted Temperature Data into Database.")

def Humidity_Data_Handler(jsonData):
    # Parse Data 
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Humidity = json_Dict['Humidity']
    
    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Humidity_Data (SensorID, Date_n_Time, Humidity) values (?,?,?)", [SensorID, Data_and_Time, Humidity])
    del dbObj
    print("Inserted Humidity Data into Database.")

def Pressure_Data_Handler(jsonData):
    # Parse Data 
    json_Dict = json.loads(jsonData)
    SensorID = json_Dict['Sensor_ID']
    Data_and_Time = json_Dict['Date']
    Pressure = json_Dict['Pressure']
    
    # Push into DB Table
    dbObj = DatabaseManager()
    dbObj.add_del_update_db_record("insert into Pressure_Data (SensorID, Date_n_Time, Pressure) values (?,?,?)", [SensorID, Data_and_Time, Pressure])
    del dbObj
    print("Inserted Pressure Data into Database.")

def sensor_Data_Handler(Topic, jsonData):
    if Topic == "Home/BedRoom/1/Temperature":
        Temp_Data_Handler(jsonData)
    elif Topic == "Home/BedRoom/1/Humidity":
        Humidity_Data_Handler(jsonData)
    elif Topic == "Home/BedRoom/1/Pressure":
        Pressure_Data_Handler(jsonData)

def display_database_contents():
    conn = sqlite3.connect(DB_Name)
    cursor = conn.cursor()
    
    print("\nTemperature Data:")
    cursor.execute("SELECT * FROM Temperature_Data")
    for row in cursor.fetchall():
        print(row)
        
    print("\nHumidity Data:")
    cursor.execute("SELECT * FROM Humidity_Data")
    for row in cursor.fetchall():
        print(row)
        
    print("\nPressure Data:")
    cursor.execute("SELECT * FROM Pressure_Data")
    for row in cursor.fetchall():
        print(row)
    
    cursor.close()
    conn.close()

def on_message(client, userdata, message):
    print("received message: ", str(message.payload.decode("utf-8")))
    sensor_Data_Handler(message.topic, message.payload)

if __name__ == "__main__":
    build_db(TableSchema)
    display_database_contents()  # Display initial database contents
    client = mqtt.Client("Sniffer")
    client.connect(mqttBroker) 

    client.subscribe(MQTT_Topic)
    client.on_message = on_message
    client.loop_forever()