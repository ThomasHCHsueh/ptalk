import os
import email
import imaplib


class Receiver:
    def __init__(self, from_whom):

        self.email = os.environ.get('MY_EMAIL')
        self.pwd   = os.environ.get('MY_PWD')
        self.from_whom = from_whom
        self.server = 'imap.gmail.com'
    
    def receive(self):
        mail = imaplib.IMAP4_SSL(self.server)
        mail.login(self.email, self.pwd)
        mail.select('inbox')

        status, data = mail.search(None, '(SUBJECT "ptalk")')
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        
        ret = []
        for idx, i in enumerate(mail_ids):
            status, data = mail.fetch(i, '(RFC822)')
            
            ## the content data at the '(RFC822)' format comes on
            ## a list with a tuple with header, content, and the closing
            ## byte b')'
            for response_part in data:
                if isinstance(response_part, tuple):
                    message = email.message_from_bytes(response_part[1])
                    
                    if not message.is_multipart():
                        continue
                    for part in message.get_payload():
                        if part.get('Content-Disposition') is None:
                            continue
                        tmp = f"./{idx}.rcv.tmp"
                        with open(tmp, 'wb') as f:
                            f.write(part.get_payload(decode=True))
            ret.append(tmp)

        ## move ptalk mails to trash
        if len(mail_ids)>0:
            start = mail_ids[0].decode()
            end = mail_ids[-1].decode()
            mail.store(f'{start}:{end}'.encode(), '+X-GM-LABELS', '\\Trash')


        return ret

if __name__ == '__main__':
    r = Receiver("")
    r.receive()
