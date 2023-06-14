import RPi.GPIO as GPIO
from datetime import datetime
import calendar

from statusLed import StatusLed
import AirthingsReader as Airthings


class logEntry:
    current_valuesA = None
    current_valuesP = None
    

    def __init__(self, config_values, session, statusLed):
        self.config_values = config_values
        self.session = session

        self.thresholdValue1 = 50
        self.thresholdValue2 = 100

        self.serial_number = str(self.config_values['serial_number'])

        self.statusLed = statusLed
        
        

    def sendData(self):
        if self.current_valuesA == None: 
            self.getDataFromAirthings()

        if self.current_valuesP == None: 
            self.getDataFromRPi()

        

        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())

        data = {
            "logger_name": self.config_values['logger_name'],
            "timestamp": unixtime,
            "humidity_inside": self.current_valuesA.humidity,
            "humidity_outside": 60,
            "temp_inside": self.current_valuesA.temperature,
            "temp_outside": 20,
            "radon_level": self.current_valuesA.radon_sta,
            "battery_status": "good"
        }

        print("sending data to API")
        try:
            response = self.session.post(self.config_values['url'] + "/user/logger/data", json = data)
            print(response.text)
            print("success")
        except: 
            print("something went wrong while sending daata")
        finally:
            print("-----------------------")
            

        
        

    def getDataFromAirthings(self):
        print("getting data from airthings")
        #connect to airthings api
        #get data and package it neatly 
        self.current_valuesA = Airthings.connectAndRead(self.serial_number)
        print(self.current_valuesA)
        
        self.setLed()
        #AirthingsReader.read()

    def getDataFromRPi(self):
        print("getting data from rpi")
        #read sensor data and package it neatly
        pass

    def setLed(self):
        #set led status in statusLed.py
        self.statusLed.setState(self.current_valuesA.radon_sta, self.thresholdValue1, self.thresholdValue2)
        