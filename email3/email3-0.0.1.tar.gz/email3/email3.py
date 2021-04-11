# @Time : 2021/4/11 12:21 
# @Author : GanJianWen
# @File : email3.py
# @Email: 1727949032@qq.com
# @Software: PyCharm

import smtplib
from email.mime.text import MIMEText
from email.header import Header


class Mailer(object):
    def __init__(self, sender_user_name, sender_password, smtp_server="smtp.qq.com"):
        self.sender_user_name = sender_user_name
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_object = smtplib.SMTP()
        self.smtp_object.connect(self.smtp_server, 25)

    def send_email(self,sender_name="email3", recipients=[], subject="hello world", message=None,encoding="utf-8",type="plain"):
        msg = MIMEText(message,type,encoding)
        msg["Subject"] = Header(subject,encoding)
        msg['From'] = Header(sender_name,encoding)
        msg["To"] = Header("你", encoding)
        self.smtp_object.login(self.sender_user_name,self.sender_password) 
        self.smtp_object.sendmail(self.sender_user_name, recipients, msg.as_string())
    
    
    def __str__(self) -> str:
        return """
                    user_name:{0}\n
                    password:{1}\n
                    stmp_server:{2}\n
               """.format(
                   self.sender_user_name,
                   self.sender_password,
                   self.smtp_server
               )

    def __del__(self):
        self.smtp_object.quit()


if __name__ == '__main__':
    mailer = Mailer("1727949032@qq.com", "kafnedgotjsgjbhg")
    mailer.send_email(sender_name="甘建文",recipients=["1727949032@qq.com"], subject="你好",message="<li>hello</li>",type="html")
