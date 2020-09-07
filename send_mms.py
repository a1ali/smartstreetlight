from twilio.rest import Client
from credentials import *


client = Client(account_sid, auth_token)

def send_sms(url, from_num):

    message = client.messages \
        .create(
             body='Heres a random pic of a dog',
             from_=my_twilio,
             media_url=[url],
             to=from_num
         )

    #print(message.sid)
