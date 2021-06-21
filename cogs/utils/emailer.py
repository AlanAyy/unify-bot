from __future__ import print_function
import os.path
from email.mime.text import MIMEText

import google_auth_httplib2
import googleapiclient
import httplib2
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from google.oauth2.credentials import Credentials

import base64

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def send_email(to, subject, message_text):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('settings/gmail_token.json'):
        creds = Credentials.from_authorized_user_file('settings/gmail_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # This causes the error
        else:
            # This is what opens the Chrome tab to request access
            flow = InstalledAppFlow.from_client_secrets_file('settings/gmail_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('settings/gmail_token.json', 'w') as token:
            token.write(creds.to_json())

    mime_text = MIMEText(message_text)
    mime_text['to'] = to
    mime_text['subject'] = subject
    body = {'raw': base64.urlsafe_b64encode(mime_text.as_bytes()).decode()}

    def build_request(http, *args, **kwargs):
        new_http = google_auth_httplib2.AuthorizedHttp(creds, http=httplib2.Http())
        return googleapiclient.http.HttpRequest(new_http, *args, **kwargs)

    # with discovery.build('gmail', 'v1', credentials=creds) as service:
    with discovery.build('gmail', 'v1', credentials=creds, requestBuilder=build_request) as service:
        # Call the Gmail API and send the email
        service.users().messages().send(userId='me', body=body).execute()
