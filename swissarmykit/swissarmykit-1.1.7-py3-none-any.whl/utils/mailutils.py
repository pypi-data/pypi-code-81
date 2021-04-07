import re
import smtplib
from validate_email import validate_email

class MailUtils:
    '''
    https://myaccount.google.com/lesssecureapps. Enable less secure app
    Under Settings Gmail. Tab Forwarding and POP/IMAP. Enable IMAP
    Also check limit rate for Gmail. 150/24hrs on Desktop, or 500/day

    '''
    def __init__(self, email=None, password=None, default='Gmail'):
        self.session = None
        self.email = None

        if email and password and default == 'Gmail':
            self.init_Gmail(email, password)

    def init_Gmail(self, email, password):
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.login(email, password)
        self.email = email
        self.session = s
        print('INFO: Login Gmail success. Account: ', self.email)

    def send(self, to, subject, body):
        if not (to and subject and body):
            raise Exception('to, subject, body fields is required')

        receiver = None
        if isinstance(to, list):
            receiver = [t.strip() for t in to]
        if isinstance(to, str):
            receiver = [t.strip() for t in re.split(";|,", to)]

        all_valid = True
        for to in receiver:
            if not validate_email(to):
                print('ERROR: Invalid email ', to)
                all_valid = False

        if not receiver or not all_valid:
            raise Exception('INFO: Please check send: to')

        msg = '''From: %s\nTo: %s\nSubject: %s\n\n%s\n''' % (self.email, ', '.join(receiver), subject, body)
        self.session.sendmail(self.email, receiver, msg)

    def close(self):
        self.session.close()

if __name__ == '__main__':
    m = MailUtils('devpython7@gmail.com', '')
    m.send('devpython7@gmail.com', subject='test python', body='From development')


