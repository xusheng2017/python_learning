

from email.mime.text import MIMEText
import smtplib

sendto_list = ['742207387@qq.com' , '2407241030@qq.com' ]

mail_host = 'smtp.qq.com'
mail_user = '742207387'
mail_passwd = 'lbwjuycnzfiubfge'
mail_postfix = 'qq.com'

send_theme = input("theme >>> ")
send_msg = input("content >>> ")

#发送邮件
def send_mail(to_list , sub , content):
	'''
	to_list:发给谁
	sub:主题
	content:内容
	send_mail('xxxx@xx.com' , '主题' , '内容')
	'''
	me = mail_user + '<' + mail_user + '@' +mail_postfix + '>'
	msg =  MIMEText(content)
	msg['subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(to_list)
	try:
		s = smtplib.SMTP_SSL(mail_host , 465)
		s.set_debuglevel(1)
		s.login(mail_user , mail_passwd)
		s.sendmail(me , to_list , msg.as_string())
		s.close()
		return True
	except Exception as e:
		print('str(e)')
		return Falsea


if __name__ == '__main__':
	if send_mail(sendto_list , send_theme , send_msg):
		print('send success')
	else:
		print('send fail')