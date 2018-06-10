

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email import encoders 
import smtplib

recv_list = ['742207387@qq.com' , '2407241030@qq.com' ]
#msg = MIMEText()


mail_host = 'smtp.qq.com'
mail_user = '742207387'
mail_passwd = 'lbwjuycnzfiubfge'
mail_postfix = 'qq.com'

#send_theme = input("theme >>> ")
#send_msg = input("content >>> ")
send_msg1 = '<html><body><h1>Hello</h1>' + '<p>百度网址： <a href="http://www.baidu.com">百度</a></p>' + '</body></html>'


#发送邮件
def send_mail(to_list , sub , content):
	'''
	to_list:发给谁
	sub:主题
	content:内容
	send_mail('xxxx@xx.com' , '主题' , '内容')
	'''
	sender = mail_user + '<' + mail_user + '@' +mail_postfix + '>'
	msg =  MIMEText(content , 'html' ,'utf-8')

#	msg = MIMEMultipart()

	msg['From'] =	Header(sender , 'utf-8')
#	print(msg['From'])
	msg['To'] = ";".join(to_list)
#	print(msg['To'])
	msg['subject'] = Header(sub , 'utf-8')
#	print(msg['subject'])
'''
	msg.attach(MIMEText(content , 'html' , 'utf-8'))
	with open('/home/python01/python/python_learning/email/test.gif','rb') as f:
		mime = MIMEBase('image' , 'gif' , filename = 'test.gif')
		mime.set_playload(f.read())
		encoders.encode_base64(mime)
		msg.attach(mime)
'''
	try:
		s = smtplib.SMTP_SSL(mail_host , 465)
		s.set_debuglevel(1)
		s.login(mail_user , mail_passwd)
		s.sendmail(sender , to_list , msg.as_string())
		s.close()
		return True
	except Exception as e:
		print('str(e)')
		return False


if __name__ == '__main__':
	if send_mail(recv_list , 'send_theme' , send_msg1):
		print('send success')
	else:
		print('send fail')






