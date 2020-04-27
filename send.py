import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email import encoders

class Sender:
    def __init__(self, text, attached, to_addr):
        self.text = text
        self.attached = attached
        self.to_addr = to_addr
        self.email = os.environ.get('MY_EMAIL')
        self.pwd   = os.environ.get('MY_PWD')

    def send(self):
        # connect with Google's servers
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465

        from_addr = self.email
        to_addrs = [self.to_addr]

        # prepare file attachment
        atta = open(self.attached, 'rb')
        p = MIMEBase('application', 'octet-stream')
        p.set_payload((atta).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', f'attachment; filename={self.attached}')

        # use MIMEText to send only text
        message = MIMEMultipart()        
        message['subject'] = 'ptalk'
        message['from'] = from_addr
        message['to'] = ', '.join(to_addrs)
        message.attach(MIMEText(self.text, 'plain'))
        message.attach(p)

        # we'll connect using SSL
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    
        # to interact with the server, first we log in
        # and then we send the message
        server.login(self.email, self.pwd)
        server.sendmail(from_addr, to_addrs, message.as_string())
        server.quit()

