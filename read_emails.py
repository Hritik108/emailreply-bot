from simplegmail import Gmail
from urllib.request import urlopen
from simplegmail.query import construct_query
from write_email import create_email
# from send_email import send_email
import schedule
import time
from datetime import datetime

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.modify']
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
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

    # messages = gmail.get_messages(query=construct_query(query_params))
    messages = gmail.get_unread_inbox(query=construct_query(query_params))
    if len(messages) == 0 :
        print("No unread message")
        return
    else:
        # return
            # message_to_read = messages[0]
            # message_to_read.mark_as_read()
        print("unread message there")
        print(len(messages))
   
        for message in messages:
            if "[Zomato] New Review for" in message.subject :
                # if "Greetings" in message.subject :
                # print("To: " + message.recipient)
                # print("From: " + message.sender)
                # print("Subject: " + message.subject)
                # print("Date: " + message.date)
                # print(message.snippet)
                # print("body is above")
                print(message.headers['Message-ID'])
                print(message.id)
                message_id=message.headers['Message-ID']
                message.mark_as_read()
                # print("Preview: " + message.snippet)
                # print("message_thread :"+message.thread_id)
                # print("message :"+message.id)
                generated_message = create_email(message.snippet)
                # # send_email( message.sender,message.subject,geneated_message)

                reply_message = EmailMessage()
                print(reply_message)
                # for p in message['payload']['headers']:
                #     if p['name']=='Message-ID' :
                #         message_id=p['value']
                #         print(message_id)
                reply_message.set_content(generated_message)

                if message.sender != "kamleshdubey108@gmail.com":
                    reply_message['To'] = message.sender
                    reply_message['From'] = "kamleshdubey108@gmail.com"
                else:
                    reply_message['To'] = message.recipient
                    reply_message['From'] = "kamleshdubey108@gmail.com"

                reply_message['Subject'] = message.subject
                # reply_message['References '] = message.id
                # reply_message['In-Reply-To '] = message.id
                reply_message['References '] = message_id
                reply_message['In-Reply-To '] = message_id

                encoded_message = base64.urlsafe_b64encode(reply_message.as_bytes()).decode()

                create_message = {'raw': encoded_message,
                            'threadId': message.thread_id}
                # Sending the reply message to the thread
                send_message = (service.users().messages().send(userId="me", body=create_message).execute())      

                print('Email has been sucessfully sent')          
                break

        #  else : print("No unread messages")
# create_email(message.b);

        # with open("email_samples.txt",'a') as f:
        #     if message.plain:
        #         if len(message.plain) < 1000:
        #             f.write(message.plain)
# print(messages[0].plain)
    
    # with open("email_samples.txt", "a") as f:
    #     if message.plain:
    #         if len(message.plain) < 1000:
    #             f.write(message.plain)
    # print("Message Body: " + message.plain)  # or message.html

# while True==True :
# read_emails()

schedule.every(1).minutes.do(read_emails)

while True:
    schedule.run_pending()
    time.sleep(1)

read_emails()