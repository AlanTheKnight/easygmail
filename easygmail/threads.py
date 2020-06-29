class Thread(object):
    """
    Represents a thread of Gmail messages. These objects are returned by the users.threads.get() API call. They
    contain references to a list of GmailMessage objects.
    """

    def __init__(self, threadObj):
        self.threadObj = copy.deepcopy(threadObj)
        self.id = threadObj["id"]
        self.snippet = threadObj["snippet"]
        self.historyId = threadObj["historyId"]
        self._messages = None

    @property
    def text(self):
        """A list of each email's body in the thread."""
        return [msg.body for msg in self.messages]

    @property
    def messages(self):
        """The GmailMessage objects of the emails in this thread, starting from the oldest at index 0 to the most
        recent."""
        if self._messages is None:
            self._messages = []

            # The threadObj returned by the list() api doesn't include the messages list, so we need to call the get() api
            self.extendedThreadObj = SERVICE.users().threads().get(userId="me", id=self.id).execute()

            for msg in self.extendedThreadObj["messages"]:
                self._messages.append(Message(msg))

        return self._messages

    def __repr__(self):
        return "Thread numMessages=%r snippet=%r" % (len(self.messages), self.snippet)

    def senders(self):
        """List of email senders in the thread (from olders to newest)."""
        senderEmails = []
        for msg in self.messages:
            if msg.sender == EMAIL_ADDRESS:
                senderEmails.append("me")
            else:
                senderEmails.append(msg.sender)
        return senderEmails

    def latestTimestamp(self):
        """Timestamp of the last message in the thread."""
        return self.messages[-1].timestamp