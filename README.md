Gmail API Email Bot
This Python script utilizes the Gmail API to read and reply to emails, specifically designed to respond to Zomato review notifications.

Dependencies
simplegmail
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client

Install the dependencies using the following command:
pip install simplegmail google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Setup
1.Obtain the client_secret.json file by following the instructions here.
2.Run the script once to generate the token.json file for authorization.

Functionality
The script performs the following actions:

1.Reads unread emails from the Gmail inbox.
2.Identifies Zomato review notifications.
3.Generates a reply using the create_email function from write_email.py.
4.Sends the generated reply to the email thread using the Gmail API.

Execution
Run the script by executing:
python read_emails.py

Ensure that the Gmail API is enabled and the necessary credentials are obtained.

Note: This script is specifically designed for Zomato review notifications and may need adjustments for other use cases.
