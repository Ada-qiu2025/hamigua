#--*--coding:utf-8 --*--

import smtplib
from email.mime.text import MIMEText
from email.header import Header

context='测试邮件'
mail_host='smtp.qq.com'
mail_user=''
mail_pass=''


sender ='Ada@google.com'
receivers = ['3109926766@qq.com']
message = MIMEText(context,'plain','utf-8')
message['From']=Header('runoob.com','utf-8')
message['To']= Header('测试','utf-8')

subject = 'Python SMTP 邮件测试'
message['Subject']=Header(subject,'utf-8')

try:
    smtplib.SMTP('localhost').sendmail(sender,receivers,message.as_string())
    print('send suceess')

except smtplib.SMTPException:
    print('send faild')