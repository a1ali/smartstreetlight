import RPi.GPIO as GPIO
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import pigpio

led = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIR, GPIO.IN)
GPIO.setup(led, GPIO.OUT)
#led = GPIO.PWM(LED, 500)
#led.start(1)
pi = pigpio.pi()
pi.set_mode(led, pigpio.OUTPUT)
pi.set_PWM_frequency(led, 8000)
pi.set_PWM_dutycycle(led, 1)


def helloworld(self, params, packet):
    print(json.loads(packet.payload))
    mypayload = json.loads(packet.payload)
    if mypayload['rpi_motion'] == 'true':
          raise_brightness()
    elif mypayload['rpi_motion'] == 'false':
          lower_brightness()
          

          
myMQTTClient = AWSIoTMQTTClient("rpi2") #tandom key can be anything
# For TLS mutual authentication
myMQTTClient.configureEndpoint("a2fj01nuikd9c7-ats.iot.us-east-2.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("root-ca.pem.txt", "private.pem.key", "certificate.pem.crt") #Set path for Root CA and provisioning claim credentials
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
 
print('Initiating Iot Core Topic')
myMQTTClient.connect()
print('connecting')

myMQTTClient.subscribe('home/motion', 1, helloworld)
print('subscribing')




def raise_brightness():
    for dc in range(0, 256, 1):
        pi.set_PWM_dutycycle(led, dc)
        time.sleep(0.01)

    #time.sleep(10)

def lower_brightness():
    for dc in range(255, 0, -1):
        pi.set_PWM_dutycycle(led, dc)
        time.sleep(0.01)
        


try:
    while True:
        time.sleep(100)
    
except KeyboardInterrupt:
    GPIO.cleanup()
