import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import argparse
from send import Sender
from recv import Receiver
from dotenv import load_dotenv

pubkeys = {
#    'confidant':
}
recipients = {
    'confidant': 'thomasleedigitalmarketing@gmail.com'
}
load_dotenv()

def parse_args():
    
    parser = argparse.ArgumentParser(description='ptalk: an private message experiment with RSA over corruptible email')
    subparsers = parser.add_subparsers(dest='mode')

    init_parser = subparsers.add_parser('init', help='generate RSA key pair')
    send_parser = subparsers.add_parser('send', help='send encrypted message')
    recv_parser = subparsers.add_parser('recv', help='receive encrypted message.')

    send_parser.add_argument('--text', type=str, help='text to be encrypted and sent to recipient')
    send_parser.add_argument('--to-whom', type=str, choices=['confidant'], help='alias of recipient')
    
    recv_parser.add_argument('--from-whom', type=str, choices=['confidant'], help='alias of sender')

    return parser.parse_args()
    
def main():
    args = parse_args()
    ENC_PATH = os.environ.get('ENC_PATH') 
    DWNLD_PATH = os.environ.get('DWNLD_PATH')

    if args.mode == 'init':
        keyPair = RSA.generate(3072)
        with open('.myPrivKey','wb') as f:
            f.write(keyPair.export_key('DER'))
        with open('myPubKey','wb') as f:
            f.write(keyPair.publickey().exportKey('DER'))
        #print(keyPair.exportKey().decode('ascii'))
        print('new key pair generated and saved.')
        print('showing public key on screen:') 
        print(keyPair.publickey().exportKey().decode('ascii'))
        return


    f = open('.myPrivKey','rb')
    privKey = RSA.import_key(f.read())
    f = open('myPubKey','rb')
    pubKey =  RSA.import_key(f.read())


    if args.mode == 'send':
        assert args.text is not None, 'text not provided. What am I encrypting?'
        assert args.to_whom is not None, "recipient's alias not provided. Whom am I sending to?"
        
        ### ECRYPT TEXT
        encryptor = PKCS1_OAEP.new(pubKey)
        encrypted = encryptor.encrypt(args.text.encode('utf8'))
        with open(ENC_PATH, 'wb') as f:
            f.write(encrypted)
        
        ### SEND ENCRYPTED TEXT OVER EMAIL
        sender = Sender(text="see attached", attached=ENC_PATH, to_addr=recipients[args.to_whom])
        sender.send()


    elif args.mode == 'recv':
        assert args.from_whom is not None, "sender's alias not provided. From whom is the inbound message?"

        ### FETCH EMAIL, EXTRACT PAYLOAD
        receiver = Receiver(args.from_whom)
        receiver.receive()

        ### DECRYPT PAYLOAD
        with open(DWNLD_PATH, 'rb') as f:
            enc_msg = f.read()
        privKey = PKCS1_OAEP.new(privKey)
        dec_msg = privKey.decrypt(enc_msg).decode("utf-8")
        print("decrypted:")
        print(f"> {dec_msg}")
        
        ### TODO: delete DWNLD_PATH file

if __name__ == '__main__':
    main()
