import RPi.GPIO as GPIO
from datetime import datetime
from piLogger import getValues
import calendar

from statusLed import StatusLed
import AirthingsReader as Airthings


class logEntry:

    
    

    def __init__(self, config_values, session, statusLed):
        
        self.config_values = config_values
        self.session = session


        self.serial_number = str(self.config_values['serial_number'])

        self.statusLed = statusLed
        
        

    def sendData(self):
        
        
        try:
            print("no data yet, getting pi data")
            current_valuesP = self.getDataFromRPi()
        except Exception as e:
            print("failure in connecting to humidity sensor")
            print("-------------------------------------------")
            print(e)


        try:
            print("no data yet, getting airthings data")
            current_valuesA = self.getDataFromAirthings()
        except Exception as e: 
            print("failure in connecting to airthings device")
            print("-------------------------------------------")
            print(e)


        d = datetime.utcnow()
        unixtime = calendar.timegm(d.utctimetuple())

        data = {
            "logger_name": self.config_values['logger_name'],
            "timestamp": unixtime,
            "humidity_inside": current_valuesA.humidity,
            "humidity_outside": current_valuesP['humidity'],
            "temp_inside": current_valuesA.temperature,
            "temp_outside": current_valuesP['temperature'],
            "radon_level": current_valuesA.radon_sta,
            "battery_status": "good"
        }

        print("sending data to API")
        print("------------------------------------------------\n" + str(data) + "\n------------------------------------------------\n")
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
        current_valuesA = Airthings.connectAndRead(self.serial_number)

        thresholdValue1 = 50
        thresholdValue2 = 100

        self.setLed(current_valuesA=current_valuesA, thresholdValue1=thresholdValue1, thresholdValue2=thresholdValue2)
        return current_valuesA


    def getDataFromRPi(self):
        print("getting data from rpi")
        #read sensor data and package it neatly
        return getValues()


    def setLed(self, current_valuesA, thresholdValue1, thresholdValue2):
        #set led status in statusLed.py
        self.statusLed.setState(current_valuesA.radon_sta, thresholdValue1, thresholdValue2)
        
        