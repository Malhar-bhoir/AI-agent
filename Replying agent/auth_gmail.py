from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'credentials.json'

creds = None

# Check if token exists
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

# If no valid creds, authenticate
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    # Save new token
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(creds.to_json())

print("Gmail authentication successful")
