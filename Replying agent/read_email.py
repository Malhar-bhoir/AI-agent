import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import google.generativeai as genai
from pyDatalog import pyDatalog

# Google API Setup
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('gmail', 'v1', credentials=creds)

# Get latest email
results = service.users().messages().list(userId='me', maxResults=1, labelIds=["INBOX"]).execute()
msg_id = results['messages'][0]['id']
msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

headers = msg['payload']['headers']
subject = [h['value'] for h in headers if h['name'] == 'Subject'][0]
sender = [h['value'] for h in headers if h['name'] == 'From'][0]
body_data = msg['payload']['parts'][0]['body']['data']
decoded_body = base64.urlsafe_b64decode(body_data).decode("utf-8")

print(f"From: {sender}\nSubject: {subject}\n\n{decoded_body}")

# Initialize First-Order Logic (FOL)
pyDatalog.create_terms('X, Y, email_received, needs_reply')

# Define a logical rule: If an email is received, it needs a reply
email_received(sender)
needs_reply(X) <= email_received(X)  # If an email is received from X, a reply is needed

# Check if the sender needs a reply
if needs_reply(sender):
    genai.configure(api_key="Enter Your Api Key")  # Replace with your Gemini API Key
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    def generate_reply(email_text, sender_name=""):
        prompt = f"""
        You are an AI email assistant. Write a polite, formal reply to this message:

        Email:
        \"\"\"{email_text}\"\"\"

        Sender: {sender_name}
        """
        response = model.generate_content(prompt)
        return response.text.strip()

    reply = generate_reply(decoded_body, sender)
    print("\n=== Suggested Reply ===\n")
    print(reply)
