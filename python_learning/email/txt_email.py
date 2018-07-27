from email.mime.text import MIMEText
msg = MIMEText('HELLO WORLD' , 'plain' , 'utf-8')


from_addr = input('from: ')
passwd = input('passwd: ')
to_addr = input('to: ')

smtp_server = input('SMTP server: ')

import smtplib

server = smtplib.SMTP(smtp_server , 25)
server.set_debuglevel(1)
server.login(from_addr,passwd)
server.sendmail(from_addr , [to_addr] , msg.as_string())
server.quit()