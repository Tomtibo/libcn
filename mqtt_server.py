import time
import json
import base64
import paho.mqtt.client as mqttClient
class CypherApp:
    def __init(self):
        ##Not tested
        pass
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            global Connected                #Use global variable
            self.connected = True                #Signal connection
        else:
            print("Connection failed")
    def on_message(self, client, userdata, message):
        try:
    #        print(message.payload)
            print(client)
            print(userdata)
            rmesg = json.loads(message.payload)
            try:
                if rmesg['curl_code']:
                    callback = json.dumps(rmesg, indent=2)
            except ArithmeticError:
                pass
            try:
                if rmesg['newblock']:
                    callback = json.dumps(rmesg, indent=2)
            except ArithmeticError:
                pass
            try:
                if rmesg['response-topic']:
                    body = rmesg['body']
        #            print(body)
                    mesg = base64.b64decode(body).decode('utf-8').replace('\n', '')
                    response = json.loads(mesg)
                    callback = json.dumps(response, indent=2)
            except ArithmeticError:
                pass
            if resp:
                print(resp)
        except:
            print('error !')
    def start(self):
        try:
            self.connected = False   #global variable for the state of the connection
            broker_address = "broker"  #Broker address
            port = 1883                         #Broker port
            client = mqttClient.Client("Python")               #create new instance
        #    client.username_pw_set(user, password=password)    #set username and password
            client.on_connect = self.on_connect                      #attach function to callback
            client.on_message = self.on_message                      #attach function to callback
            client.connect(broker_address, port=port)          #connect to broker
            client.loop_start()        #start the loop
            while self.connected != True:    #Wait for connection
                time.sleep(0.1)
            client.subscribe("#")
        except ConnectionError:
            print('Erreur de connection')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("exiting")
            client.disconnect()
            client.loop_stop()
