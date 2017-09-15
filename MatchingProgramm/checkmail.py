import email
import imaplib
from django.db import connection
import mysql.connector


EMAIL_ACCOUNT = "iotsendmails@gmail.com"
PASSWORD = "iotss17pjs"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select('inbox')
result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
i = len(data[0].split())

subject = [] 

for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
    # this might work to set flag to seen, if it doesn't already
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
#    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject.append(str(email.header.make_header(email.header.decode_header(email_message['Subject']))))

cnx = mysql.connector.connect(user='root', password='iot17', host='127.0.0.1', database='website')
cursor = cnx.cursor()

for item in subject:

     change_status = 'UPDATE orders SET status="done" WHERE id="{}" AND status="in production"'.format(int(item))
     cursor.execute(change_status)
     cnx.commit()
cursor.close()