import smtplib

from_addr = 'iotsendmails@gmail.com'
to_addr_list = 'cn.popp@gmail.com'
cc_addr_list = ''

subject = 'Hallo'
message = 'Test'

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