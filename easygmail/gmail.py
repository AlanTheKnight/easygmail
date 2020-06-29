import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Gmail(object):
    SCOPES = ['https://mail.google.com/']
    SERVICE = None
    USER = None

    def __init__(self):
        self.build_service()

    def get_credentials(self):
        creds = None
        # If token.pickle exists, load the token.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # Otherwise, log in the user.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def build_service(self) -> None:
        self.SERVICE = build('gmail', 'v1', credentials=self.get_credentials())
        self.USER = self.SERVICE.users().getProfile(userId='me')


# def remove_labels(messages: list, labels: list) -> None:
#     """
#     Remove labels from a list of messages.
#     """
#     removeUnreadLabelObj = {"removeLabelIds": labels, "addLabelIds": []}
#     for obj in messages:
#         if isinstance(obj, Thread):
#             SERVICE.users().threads().modify(userId='me', id=obj.id, body=removeUnreadLabelObj).execute()
#         elif isinstance(obj, Message):
#             SERVICE.users().messages().modify(userId='me', id=obj.id, body=removeUnreadLabelObj).execute()


# def add_labels(messages: list, labels: list) -> None:
#     """
#     Add labels to a list of messages.
#     """
#     removeUnreadLabelObj = {"removeLabelIds": [], "addLabelIds": labels}
#     for obj in messages:
#         if isinstance(obj, Thread):
#             SERVICE.users().threads().modify(userId='me', id=obj.id, body=removeUnreadLabelObj).execute()
#         elif isinstance(obj, Message):
#             SERVICE.users().messages().modify(userId='me', id=obj.id, body=removeUnreadLabelObj).execute()


# def get_all_labels():
#     response = SERVICE.users().labels().list(userId='me').execute()
#     return {i['name']: i['id'] for i in response['labels']}
