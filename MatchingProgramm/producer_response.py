from imbox import Imbox

# SSL Context docs https://docs.python.org/3/library/ssl.html#ssl.create_default_context

imbox = Imbox('imap.gmail.com',
		username='iotsendmails@gmail.com',
		password='iotss17pjs',
		ssl=True,
		ssl_context=None)

# Gets all messages
messages_from = imbox.messages(sent_from='kristofreitz@gmx.de')

for uid, message in messages_from:
    print(message.subject)