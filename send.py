
import smtplib
from email.mime.text import MIMEText

def main():

    # connect with Google's servers
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465

    # use username or email to log in
    username = 'thomasleedigitalmarketing@gmail.com'
    password = 'Thomas1125[]'

    from_addr = 'thomasleedigitalmarketing@gmail.com'
    to_addrs = ['syr.shuyiran@gmail.com']

    # use MIMEText to send only text
    message = MIMEText('Hello this is sent from a Python practice.')
    message['subject'] = 'Hello from Python'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    # we'll connect using SSL
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    
    # to interact with the server, first we log in
    # and then we send the message
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()


if __name__ == '__main__':
    main()
