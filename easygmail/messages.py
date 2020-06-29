import datetime
import copy
import base64
import os
from .exceptions import GmailException
from . import utils
from . import parcer


class Message(object):
    """
    A Gmail message object returned by get() API call.

    Attributes:
        service - gmail service object
        message - message object
        parcer - parcer class

        id - id of the message
        thead_id - id of a thread the message belongs to
        labels - list of labels set to the message

        subject - subject of the message
        snippet - snippet of the message
        timestamp - a time when the message was sent
        sender - a sender of the message
        recipient - a recipient of the message

        body - body of a message

        attachments - list of attachments of the message

    """
    def __init__(self, service, message):
        self.servise = service
        self.message = copy.deepcopy(message)
        self.id = message["id"]
        self.thread = message["threadId"]
        self.snippet = message["snippet"]
        self.historyId = message["historyId"]
        self.timestamp = datetime.datetime.fromtimestamp(int(message["internalDate"]) // 1000)
        self.size = utils.get_message_size(message["sizeEstimate"])
        self.body = None
        self.html = None
        self.subject = None
        self.sender = None
        self.recipient = None
        self.attachments = []
        self.parcer = parcer.Parcer(self)

    def __repr__(self):
        return "Message from=%r to=%r timestamp=%r subject=%r snippet=%r" % (
            self.sender,
            self.recipient,
            self.timestamp,
            self.subject,
            self.snippet,
        )

    def __str__(self):
        return self.__repr__()

    @property
    def filenames(self):
        """Return list of attachments' filenames."""
        return [self.attachments[i]['filename'] for i in self.attachments]

    def get_files(self):
        return [
            Attachment(self.attachments[i], self) for i in self.attachments
        ]


class Attachment(object):
    def __init__(self, info, message):
        self.service = message.service
        self.message_id = message.id
        self.id = info['id']
        self.size = utils.get_message_size(info['size'])
        self.filename = info['filename']

    def download(self, folder: str, overwrite: bool = False):
        if not overwrite and os.path.isfile(os.path.join(folder, self.filename)):
            raise GmailException("File with name %s already exists." % self.filename)
        if os.path.isfile(folder):
            raise GmailException("%s is file, not a folder." % folder)
        if not os.path.exists(folder):
            os.mkdir(folder)

        attachment = self.service.users().messages().attachments().get(
            id=self.id, messageId=self.message_id, user='me')
        attachment = base64.urlsafe_b64decode(attachment["data"])

        with open(os.path.join(self.folder, self.filename), "wb") as f:
            f.write(attachment)

    def __str__(self):
        return self.filename
