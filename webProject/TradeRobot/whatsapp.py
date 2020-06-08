from twilio.rest import Client

account_sid="AC914de3d00f9c4f9b6d662b10ebe6e9bc"
auth_token="4de554bb2225fdf734bd2237220a25be"
client=Client(account_sid,auth_token)


def send_message(msg):
    from_whatsapp_number='whatsapp:+14155238886'
    to_whatsapp_number='whatsapp:+905372756330'
    client.messages.create(body=msg,from_=from_whatsapp_number,to=to_whatsapp_number)

