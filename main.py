from loggerDevice import LoggerDevice
from statusLed import StatusLed
from configEdit import ConfigEdit
import threading
import time


config_file = "logger.conf"
statusLed = StatusLed()
loggerDevice = LoggerDevice(statusLed=statusLed)


def loggerApp():
    retries = 3
    print("starting logger ...")

    

    #main loop
    while True:
        print("===============================starting===============================")
        retryCounter = 0
        tryAgain = True

        #try to create a log entry and sending to api
        while tryAgain:
            try:
                loggerDevice.log() 
                tryAgain = False
            except:
                retryCounter += 1

                #retry as long as stated on top 
                if retryCounter == retries:
                    tryAgain = True

                print("something went wrong. Trying again in 5 minutes")

                #wait a bit for the next retry
                time.sleep(10)
        #wait half an hour for the next log entry
        
        time.sleep(50)


def blinkStatusLed():
    while True:
        statusLed.setStatus(True)
        time.sleep(0.1)
        statusLed.setStatus(False)
        time.sleep(5)



def confEditor():
    ConfigEdit(config_file=config_file)
    print("conf edit started")




def main (): 
    thread1 = threading.Thread(target=blinkStatusLed)
    thread1.start()

    # Create and start the second thread
    thread2 = threading.Thread(target=confEditor)
    thread2.start()

    loggerApp()


if __name__ == "__main__": 
    main ()