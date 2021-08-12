# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = '***************************'
auth_token = '***************************'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="An unknown person is waiting at the entrance. Need your attention!",
                     from_='+1*********',
                     to='+91**********'
                 )

print(message.sid)