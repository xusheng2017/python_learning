

from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import smtplib

sendto_list = ['1599297609@qq.com'，'742207387@qq.com']

mail_host = 'smtp.qq.com'
mail_user = '742207387'
mail_passwd = 'lbwjuycnzfiubfge'
mail_postfix = 'qq.com'

send_theme = input("theme >>> ")                
#send_msg = input("content >>> ")

#send_msg = '<html><body><h1>Hello</h1>' + '<p>百度网址： <a href="http://www.baidu.com">百度</a></p>' + '</body></html>'
send_html_msg = '<html><body><h1>王芳是瓜皮</h1>' + '<p><img src="cid:0"></p>' + '</body></html>'
#发送邮件
def send_mail(to_list , sub , content):
	'''
	to_list:发给谁
	sub:主题
	content:内容
	send_mail('xxxx@xx.com' , '主题' , '内容')
	'''
	me = mail_user + '<' + mail_user + '@' +mail_postfix + '>'
#	msg =  MIMEText(content)
	msg = MIMEMultipart()
	msg['subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)

#邮件正文
	msg.attach(MIMEText(content , 'html' , 'utf-8'))

#构造附件1

#	with open('/home/python01/python/python_learning/email/test.txt' , 'r') as f:
#		fujian_1 = MIMEText(f.read())
#	fujian_1 = MIMEText(open('/home/python01/python/python_learning/email/test.txt' , 'rb').read() , 'base64' , 'utf-8')
#	fujian_1['Content-Type'] = 'applicattion/octet-stream'
#	fujian_1['Content-Disposition'] = 'attachment; filename = "test.txt"'
#	msg.attach(fujian_1)

#构造附件2
	with open('/home/python01/python/python_learning/email/test.gif' , 'rb') as f:
		picture = MIMEBase('image' , 'gif' , filename = "test.gif")
		picture.add_header('Content-Disposition' , 'attachment' ,filename = "123.jpg")
		picture.add_header('Content-ID' , '<0>')
		picture.add_header('X-Attachment-ID' , '0')
		picture.set_payload(f.read())
		encoders.encode_base64(picture)
		msg.attach(picture)


#构造附件3
#	my_jpg = MIMEText(open('/home/python01/python/python_learning/email/123.jpg','rb').read(),'base64','utf-8')
#	my_jpg['Content-Type'] = 'application/octet-stream'
#	my_jpg['Content-Disposition'] = 'attachment;filename = "123.jpg"'
#	msg.attach(my_jpg)


#构造附件4

	try:
		s = smtplib.SMTP_SSL(mail_host , 465)
		s.set_debuglevel(1)
		s.login(mail_user , mail_passwd)
		s.sendmail(me , to_list , msg.as_string())
		s.close()
		return True
	except Exception as e:
		print('str(e)')
		return False


if __name__ == '__main__':
	if send_mail(sendto_list , send_theme , send_html_msg):
		print('send success')
	else:
		print('send fail')