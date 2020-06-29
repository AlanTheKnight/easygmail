from .exceptions import GmailException
from . import Gmail
from . import messages
from . import threads


class MessagesSearch(object):
    has_next_page = False
    next_page_token = None
    pages = None
    page = None
    results = None
    kwargs = {}

    def __init__(self, gmail: Gmail, max_results=25, labels=None, query=None):
        self.service = gmail.SERVICE
        self.kwargs["maxResults"] = max_results
        if labels:
            self.kwargs["labelIds"] = labels
        if query:
            self.kwargs["q"] = query
        self.search()

    def search(self):
        self.page = 0
        response = self.service.users().messages().list(
            userId='me', **self.kwargs).execute()
        self.has_next_page = "nextPageToken" in response
        self.next_page_token = response.get("nextPageToken")
        self.pages = response['resultSizeEstimate']
        self.results = response['messages']
        return self.results

    def next_page(self):
        if not self.has_next_page:
            raise GmailException("Next page of search results doesn't exist.")
        self.kwargs["pageToken"] = self.next_page_token
        response = self.service.users().messages().list(
                userId='me', **self.kwargs).execute()
        self.page += 1
        self.has_next_page = "nextPageToken" in response
        self.next_page_token = response.get("nextPageToken")
        self.results = response['messages']
        return self.results

    def get_messages(self):
        return [
            messages.Message(
                self.service,
                self.service.users().messages().get(userId='me', id=i['id']).execute()
            ) for i in self.results
        ]

    def get_message(self, index) -> messages.Message:
        return messages.Message(
            self.service,
            self.service.users().messages().get(
                userId='me', id=self.results[index]['id']).execute()
        )
