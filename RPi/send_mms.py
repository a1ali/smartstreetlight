from twilio.rest import Client
from credentials import *


client = Client(account_sid, auth_token)

def send_sms(url, from_num):

    message = client.messages \
        .create(
             body='Image Sent',
             from_=my_twilio,
             media_url=[url],
             to=from_num
         )
    print('message Sent')

    #print(message.sid)
