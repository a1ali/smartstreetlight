'''

Added OpenCv detection and taking a picture when the takepic key is set to on from aws iot
the image will save in images and its name will be c1.png 

in the end our mqtt message will be given as 

{
  "from": "senders phone number",
  "message": "off",
  "takepic": "false",
  "motion_detected": "true/false"
}


https://stackoverflow.com/questions/53137197/importing-opencv-in-python-idle-error-shared-object-file/60237868#60237868 #how to get OpenCv on Rpi
https://github.com/amymcgovern/pyparrot/issues/34 #dependencies to install to get OpenCV to work
https://github.com/priya-dwivedi/Deep-Learning/tree/master/parking_spots_detector #sample parking code

'''

import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import RPi.GPIO as GPIO
import time

import cv2
from upload_img_s3 import upload_img
from send_mms import send_sms

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT) #using GPIO18 for testing




mypayload = {'message': None, 'takepic': None, 'from':None, 'motion_detected': None}

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

    
    #if takepic key is given as true in the mqtt message it will take a picture    
    if mypayload['takepic'] == 'true':
        cv2.imwrite('images/c1.png',frames)
        url = upload_img() #uploads the image to s3 and returns url
        send_sms(url, mypayload['from'] ) #sends sms with twilio

        



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

#print('publishing message  from RPi')

'''
myMQTTClient.publish(
    topic='home/helloworld',
    QoS=1,
    payload='{"message":"Sent from rpi"}'
    )  # this is the function to publish to a topic

'''

cap = cv2.VideoCapture(0)
car_cascade = cv2.CascadeClassifier('car2.xml') 

while True:
    # reads frames from a video 
    ret, frames = cap.read() 
      
    # convert to gray scale of each frames 
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY) 
      
  
    # Detects cars of different sizes in the input image 
    cars = car_cascade.detectMultiScale(gray, 1.1, 1) 
      
    # To draw a rectangle in each cars 
    for (x,y,w,h) in cars: 
        cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2) 
  
   # Display frames in a window  
    cv2.imshow('video2', frames)

    #if mypayload['takepic'] == 'true':
        #cv2.imwrite('images/c1.png',frames)
      
    # Wait for Esc key to stop 
    if cv2.waitKey(33) == 27: 
        break
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()
GPIO.cleanup()


    
