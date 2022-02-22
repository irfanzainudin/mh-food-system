from twilio.rest import Client

account_sid = "AC8973ba588b7ccf118d1237798a507124"
auth_token = "508360b6cc07e3b3682ad2f779c1a2f2"
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_="whatsapp:+14155238886",
    body="Test",
    to="whatsapp:+61401570603",
)

print(message.sid)
