from twilio.rest import Client

from .config import load_config

def send_message(message):
    config = load_config()

    client = Client(config.twilio_sid, config.twilio_token)
    message = client.messages.create(
        to=config.sms_destination, 
        from_='15005550006', #test
        #from_="+12244125505",
        body=message)

    print(message)
    