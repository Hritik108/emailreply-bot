from simplegmail import Gmail
from simplegmail.query import construct_query
from write_email import create_email
from datetime import datetime

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64

SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.modify']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

"""Authorization and Authentication of Account to Access GMAIL API """

# Set up the Gmail API client
service = build('gmail', 'v1', credentials=creds)


gmail = Gmail()

def read_emails():
    current_time = datetime.now().strftime("%H:%M:%S")
    print("ran at "+current_time)
    query_params = {
        "newer_than": (1, "day"),
        "older_than": (0, "day"),
    }
    messages = gmail.get_unread_inbox(query=construct_query(query_params))
    if len(messages) == 0 :
        return
    else:
        for message in messages:
            if "[Zomato] New Review for" in message.subject :
                print("customer: "+message.snippet)
                message_id=message.headers['Message-ID']
                generated_message = create_email(message.snippet)
                reply_message = EmailMessage()
                print("botReply: "+generated_message)
                reply_message.set_content(generated_message)

                if message.sender != "kamleshdubey108@gmail.com":
                    reply_message['To'] = message.sender
                    reply_message['From'] = "kamleshdubey108@gmail.com"
                else:
                    reply_message['To'] = message.recipient
                    reply_message['From'] = "kamleshdubey108@gmail.com"

                reply_message['Subject'] = message.subject
                reply_message['References '] = message_id
                reply_message['In-Reply-To '] = message_id

                encoded_message = base64.urlsafe_b64encode(reply_message.as_bytes()).decode()

                create_message = {'raw': encoded_message,
                            'threadId': message.thread_id}
                # Sending the reply message to the thread
                service.users().messages().send(userId="me", body=create_message).execute()     
                message.mark_as_read()
                print('Email has been sucessfully sent')          
                break

read_emails()