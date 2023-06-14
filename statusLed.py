import RPi.GPIO as GPIO


class StatusLed:

    def __init__(self):
        #define variables
        self.red = 16
        self.yellow = 20
        self.green = 21
        self.blue = 26

        #gpio setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        #IO
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.yellow, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)

        


    def setState(self, radonLevel, thresholdValue1, thresholdValue2):
        if (radonLevel > thresholdValue2):
            self.StateRed()
        elif (radonLevel > thresholdValue1 & radonLevel <= thresholdValue2):
            self.StateYellow()
        else: 
            self.StateGreen()


    def setStatus(self, state):
        #setStatusLedOn
        GPIO.output(self.blue, state)



#Led states

    def StateRed (self):
        GPIO.output(self.red, True)
        GPIO.output(self.yellow, False)
        GPIO.output(self.green, False)

    def StateYellow (self):
        GPIO.output(self.red, False)
        GPIO.output(self.yellow, True)
        GPIO.output(self.green, False)

    def StateGreen (self):
        GPIO.output(self.red, False)
        GPIO.output(self.yellow, False)
        GPIO.output(self.green, True)
