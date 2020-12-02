import os
import sys
import pickle
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText

def get_gmail_api_instance():
	"""
	Setup Gmail API instance
	"""
	if not os.path.exists('token.pickle'):
		return None
	with open('token.pickle', 'rb') as token:
		creds = pickle.load(token)
	service = build('gmail', 'v1', credentials=creds)
	return service

def create_message(sender, to, subject, message_text):
	"""
	Create a message for an email
		:sender: (str) the email address of the sender
		:to: (str) the email address of the receiver
		:subject: (str) the subject of the email
		:message_text: (str) the content of the email
	"""
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	raw = base64.urlsafe_b64encode(message.as_bytes())
	raw = raw.decode()
	body = {'raw': raw}
	return body

def send_email(service, user_id, message):
	"""
	Send an email via Gmail API
		:service: (googleapiclient.discovery.Resource) authorized Gmail API service instance
		:user_id: (str) sender's email address, used for special "me" value (authenticated Gmail account)
		:message: (base64) message to be sent
	"""
	try:
		message = (service.users().messages().send(userId=user_id, body=message).execute())
		return message
	except Exception as e:
		print("err: problem sending email")
		print(e)

def main():
	"""
	Set up Gmail API instance, use it to send an email
	  'sender' is the Gmail address that is authenticated by the Gmail API
	  'receiver' is the receiver's email address
	  'subject' is the subject of our email
	  'message_text' is the content of the email
	"""
	# draft our message
	sender = 'pythonista@gmail.com'
	receiver = 'receiver@gmail.com'
	subject = 'Just checking in!'
	message_text = "Hi! How's it going?"

	# authenticate with Gmail API
	service = get_gmail_api_instance()
	if service == None:
		print("err: no credentials .pickle file found")
		sys.exit(1)

	# create message structure
	message = create_message(sender, receiver, subject, message_text)

	# send email
	result = send_email(service, sender, message)
	if not result == None:
		print(f"Message sent successfully! Message id: {result['id']}")

if __name__ == '__main__':
	main()