from __future__ import print_function

import logging
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def check_notifications():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', cache_discovery=False, credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(maxResults=50, userId='me', q='from:notify@goabode.com is:unread').execute()
    message_ids = results.get('messages', [])
    notifications = []
    if not message_ids:
        logging.debug('No messages found.')
    else:
        for message_id in message_ids:
            message = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()
            payload = message['payload']
            headers = payload['headers']
            for d in headers:
                if d['name'] == 'Subject':
                    # To have the oldest at the front of the list, insert at 0 index
                    notifications.insert(0, d['value'])
                    service.users().messages().trash(userId='me', id=message_id['id']).execute()
    return notifications


