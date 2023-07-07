import logging
from azure.communication.chat import ChatClient
from twilio.rest import Client
import openai

# Set up Azure Communication Services
endpoint = "https://claimsstatuscommservice.communication.azure.com"  # Replace with your Azure Communication Services endpoint
access_key = "xMdYfkRk71R0Rr7IBCgc4GKzKr1PWxEBzs3EseQSaEKMVxr0hjXET47aMBMDZGn+vQ7r1+xjXCVxVC3+7sc1tg=="  # Replace with your Azure Communication Services access key
chat_client = ChatClient(endpoint, access_key)

# Set up Twilio
account_sid = "ACd9a2cfc0ad4f0235c94c717d2bf9f33a"  # Replace with your Twilio account SID
auth_token = "0da96bf84014f9e91e8d420eb0533888"  # Replace with your Twilio auth token
twilio_phone_number = "+18559654331"  # Replace with your Twilio phone number
twilio_client = Client(account_sid, auth_token)

# Set up OpenAI
openai.api_key = "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"  # Replace with your OpenAI API key
print("Who is this?1")
# Define a function to handle incoming messages
def handle_incoming_sms(sender, message):
    # Send the user's message to OpenAI for processing
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot."},
            {"role": "user", "content": message},
        ],
    )
    bot_response = response.choices[0].message.content

    # Send the bot's response back to the user via Azure Communication Services
    chat_client.send_message(to=sender, content=bot_response)

    # Return the bot's response
    return bot_response

def main(req):
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        sender_phone_number = req_body.get('sender_phone_number')
        incoming_message = req_body.get('incoming_message')

        if sender_phone_number and incoming_message:
            bot_response = handle_incoming_sms(sender_phone_number, incoming_message)
            return f"Bot's response: {bot_response}"
        else:
            return "Please provide 'sender_phone_number' and 'incoming_message' in the request body."
    except Exception as e:
        logging.error(str(e))
        return "Internal Server Error"