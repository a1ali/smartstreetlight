import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)



mypayload = {'message': None}

def helloworld(self, params, packet):
    global mypayload
    print('Received message from AWS IoT Core')
    print('Topic: ' + packet.topic)
    #print('Payload: ',json.loads(packet.payload) )
    
    mypayload = json.loads(packet.payload)
    print(mypayload)
    if mypayload['message'] == 'on':
        print('led on')
        GPIO.output(18,GPIO.HIGH)

    if mypayload['message'] == 'off':
        print('led off')
        GPIO.output(18,GPIO.LOW)



# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("clientidrpi") #tandom key can be anything
# For TLS mutual authentication
myMQTTClient.configureEndpoint("a2fj01nuikd9c7-ats.iot.us-east-2.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("/home/pi/awsiot/root-ca.pem", "/home/pi/awsiot/private.pem.key", "/home/pi/awsiot/certificate.pem.crt") #Set path for Root CA and provisioning claim credentials
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
 
print('Initiating Iot Core Topic')
myMQTTClient.connect()

myMQTTClient.subscribe('home/helloworld', 1, helloworld)

print('publishing message  from RPi')
'''
myMQTTClient.publish(
    topic='home/helloworld',
    QoS=1,
    payload="{'Message':'Sent from rpi}"
    )  # this is the function to publish to a topic
'''
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()


    
