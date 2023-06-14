import board 
import busio
import adafruit_am2320
import time



print("setting up i2c")
i2c = busio.I2C(board.SCL, board.SDA)


try:
    sensor = adafruit_am2320.AM2320(i2c)
    humidity = sensor.relative_humidity
    time.sleep(0.1)
    temp = sensor.temperature
    time.sleep(0.1)
except Exception as e:
    print(e)



def getValues ():
    
    data = {
        'humidity': humidity,
        'temperature': temp
    }
    return data

    