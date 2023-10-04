import Adafruit_DHT
from time import time, sleep
from urllib.request import urlopen
import sys
import bmpsensor
from Adafruit_CharLCD import Adafruit_CharLCD

# instantiate lcd and specify pins
lcd = Adafruit_CharLCD(rs=26, en=19,
                       d4=13, d5=6, d6=5, d7=11,
                       cols=16, lines=2)
lcd.clear()

# display text on LCD display
lcd.message('Weather Monitor-\n ing System')




WRITE_API = "BO4JIZA28CMDZMSK" # Replace your ThingSpeak API key here
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)



SENSOR_PIN = 4
SENSOR_TYPE = Adafruit_DHT.DHT11

SensorPrevSec = 0
SensorInterval = 2 # 2 seconds
ThingSpeakPrevSec = 0
ThingSpeakInterval = 15 # 15 seconds

try:
    while True:
        
        if time() - SensorPrevSec > SensorInterval:
            SensorPrevSec = time()
            
            humidity, temperature = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
            pressure, altitude = bmpsensor.readBmp180()
            print("Temperature = {:.2f} C".format(temperature))
            print("Humidity = {:.2f} %".format(humidity))
            print("Pressure = {:.2f} Pa".format(pressure)) # Pressure in Pa
            print("Altitude = {:.2f} m".format(altitude)) # Altitude in meters
            print("\n")            
            
        if time() - ThingSpeakPrevSec > ThingSpeakInterval:
            ThingSpeakPrevSec = time()
            
            thingspeakHttp = BASE_URL + "&field1={:.2f}".format(temperature) + "&field2={:.2f}".format(humidity) + "&field3={:.2f}".format(pressure) + "&field4={:.2f}".format(altitude)
            print(thingspeakHttp)
            
            conn = urlopen(thingspeakHttp)
            print("Response: {}".format(conn.read()))
            conn.close()
            
            
            sleep(1)
            
except KeyboardInterrupt:
    conn.close()
    

