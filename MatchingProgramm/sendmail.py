import smtplib
import mysql.connector

# Connection to database
cnx = mysql.connector.connect(user='root', password='iot17', host='127.0.0.1', database='website')
cursor = cnx.cursor()

# get orders with in production
cursor.execute("SELECT m.order_id, ma.producer_id from matches m, orders o, machines ma WHERE o.status='in production' AND o.id=m.order_id AND ma.id=m.machine_id")
send_orders = cursor.fetchall()

# get mail recipient
for item in send_orders:
    query = 'SELECT p.email FROM producers p WHERE p.id="{}"'.format(item[1])
    cursor.execute(query)
    mailAddress = cursor.fetchall()
    
    # send mail
    from_addr = 'iotsendmails@gmail.com'
    to_addr_list = mailAddress[0]
    cc_addr_list = ''
    
    subject = item[0]
    message = 'Please produce the order in the subject.'
    
    login = 'iotsendmails@gmail.com'
    password = 'iotss17pjs'
    smtpserver='smtp.gmail.com:587'
    
    header = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
    
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    problems = server.sendmail(from_addr, to_addr_list, message)
server.quit()