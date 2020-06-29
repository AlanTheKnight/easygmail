# EasyGmail

Library for retrieving and sending mail using Gmail API.

## Examples

```python
import easygmail
from easygmail import mailbox

gmail = easygmail.Gmail()

# Performing search - unread messages
search = mailbox.MessagesSearch(labels=["UNREAD"])
print(search.results)
m = search.get_message(0) # Let's get the first message
print("From:", m.sender) # Sender
if m.html is not None: # HTML content of the message
    with open("content.html", "w") as f:
        f.write(m.html)
```

