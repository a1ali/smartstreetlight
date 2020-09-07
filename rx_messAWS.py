from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from get_dog import get_dog_url
from send_mms import send_sms

import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


#this functions is the response function to an MQTT message it is manadatory to have in the myMQTTClient.subscribe
def helloworld(self, params, packet):
    print('Received message from AWS IoT Core')
    print('Topic: ' + packet.topic)
    print(packet.payload)
    return ""


#this is basic setup to initialize AWS IoT
# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("clientidcomp") #tandom key can be anything
# For TLS mutual authentication
myMQTTClient.configureEndpoint("a2fj01nuikd9c7-ats.iot.us-east-2.amazonaws.com", 8883) #Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("root-ca.pem.txt", "private.pem.key", "certificate.pem.crt") #Set path for Root CA and provisioning claim credentials
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
 
print('Initiating Iot Core Topic')
myMQTTClient.connect() #important connection call to AWS


#myMQTTClient.subscribe('home/helloworld', 1, helloworld) #the format of subscribing is (topic, 1, function)
#print('sending mess')
'''
myMQTTClient.publish(
    topic='home/helloworld',
    QoS=1,
    payload="{'Message: from computer'}" #the payload must be in JSON format to be able to be used. DO NOT FORGET!!!
)
'''
#function to publish a turn on message 
def ledon():
    mes = {
        "message": "on"
    }
    message = json.dumps(mes)
    myMQTTClient.publish(
    topic='home/helloworld',
    QoS=1,
    #payload='{"message": "on"}'
    payload=jsonify(message='on')
    )
    #print('sending led on ')
    #print(message)
    return ""

#function to publish turn off message
def ledoff():

    myMQTTClient.publish(
    topic='home/helloworld',
    QoS=1,
    payload='{"message": "off"}'
    )
    return ""


#flask webserver initiailizing rember in Twilio message comes in webhook to include the /sms after link
app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    '''Respond to incoming messages with a friendly sms.'''
    greetings = ['hello', 'hi', 'hii', 'hola', 'hello!', 'hey', 'heyy', 'hey!' ]
    #start the responsse
    resp = MessagingResponse() #this is twilio response initializing 
    x = request.form.to_dict() #take a request to our webserver and turn it into python dict
    print(x)
    print('\n')
    print(x['Body']) #the message will be in the body key.
    print(f"from {x['From']}")

    message = x['Body'].lower() #turn the message to lower case 
    message = ''.join(message.split()) # sometimes the user puts extra spaces and we have to trip them 
    body = u'Sending you a dog picture soon \U0001F415 \U0001F436'

    print(message.lower())
    

    if message in greetings:
        body = 'Hello There!'

    elif message == "bye":
        body = "Goody Bye"

    elif message == '!help':
        body = 'Enter a Street Adress as follows \nAddress/City/State/Zip'

    elif message == '!dog':
        send_sms(get_dog_url(),x['From'] )
        
    elif message == 'on':
        #message = json.dumps(mes)
        myMQTTClient.publish(
        topic='home/helloworld',
        QoS=1,
        payload='{"message": "on"}'
        #payload=jsonify(message='on')
        )
        
    elif message == 'off':
        myMQTTClient.publish(
        topic='home/helloworld',
        QoS=1,
        payload='{"message": "off"}'
        )
    
    

    print(message)

    #Add a message
    #resp.message(body) #thsi is to send the sms by responsing to client

    return ""  



if __name__ == "__main__":
    app.run(debug=True)









    '''
so to run this program we take advantage of flask and serveo.net we use the command 

ssh -o ServerAliveInterval=30 -R smartstreetlightaa.serveo.net:80:127.0.0.1:5000 serveo.net

to create a server that can then allow us to forward all requests to it 
    '''
