import configparser
import requests
from logEntry import logEntry

class LoggerDevice (): 
    
    
    def __init__ (self, statusLed):
        self.session = requests.session()
        self.statusLed = statusLed


        #get data from config
        self.config_values = self.getLocalData()

        self.getInfoFromApi()



    def log (self): 
    
        #log in to api with credentials from config
        self.login()
       

        #initiate logEntry class and create log entry
        self.logEntry = logEntry(self.config_values, self.session, self.statusLed)
        self.createLogEntry()
        




    def getLocalData (self):
        print("reading config...")

        config = configparser.ConfigParser()
        config.read("logger.conf")
        
        # Retrieve values from the config file
        server = config.get('DEFAULT', 'url')
        logger_name = config.get('DEFAULT', 'loggerName')
        user_name = config.get('DEFAULT', 'userName')
        password = config.get('DEFAULT', 'password')
        serial_number = config.get('DEFAULT', 'serialNumber')
        
        # Return the values as a dictionary
        config_values = {
            'url': server,
            'logger_name': logger_name,
            'user_name': user_name,
            'password': password,
            'serial_number': serial_number
        }
        print(config_values)
        print("-----------------------\n")
        return config_values


    def login (self):
        print("logging in...")

        data = {
            'username': self.config_values['user_name'],
            'password': self.config_values['password'],
            'hashedData': 'sigridkeyeasteregg'
        }
        
        try: 
            response = self.session.post(self.config_values['url'] + "/user/login", json = data)
            print(response)
            if response.status_code == 200:
                self.loggedIn = True
                print("success")
            else:
                print("something went wrong in login")
        except: 
            print("something went wrong \n\n\n")
            
        print("-----------------------\n")


    def getInfoFromApi (self):
        print("fetching data about logger...")

        data = {
            'data_logger_name' : self.config_values['logger_name']
        }
        response = self.session.post(self.config_values['url'] + "/user/loggers/info", json = data)

        print(response)
        print("-----------------------\n")



    def createLogEntry(self):
        print("gathering data from sensors")

        self.logEntry.sendData()
        


    # def getDataFromApiHistory (self):
    #     print("debugging historical data endpoint...")

    #     headers = {
    #         'data-logger-name' : self.config_values['logger_name']
    #     }
    #     response = self.session.get(self.config_values['url'] + "/user/logger/data", headers=headers)

    #     print(response)
    #     print(response.text)
    #     print("-----------------------\n")


       