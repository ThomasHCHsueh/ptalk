from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import argparse

my_email = 'me@mail.com'
pubkeys = {
    'confidant':
}

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

    if args.mode == 'init':
        keyPair = RSA.generate(3072)
        f = open('mykey.pem','wb')
        f.write(keyPair.export_key('PEM'))
        f.close()
        #print(keyPair.exportKey().decode('ascii'))
        print('new key pair generated and saved.')
        print('showing public key on screen:') 
        print(keyPair.publickey().exportKey().decode('ascii'))
        return

    f = open('mykey.pem','r')
    key = RSA.import_key(f.read())

    if args.mode == 'send':
        assert args.text is not None, 'text not provided. What am I encrypting?'
        assert args.to_whom is not None, "recipient's alias not provided. Whom am I sending to?"
        print(f'encrypting {args.text} now ...')
        
        ### ECRYPT TEXT
        #msg = b'A message for encryption'
        encryptor = PKCS1_OAEP.new(pubkeys[args.to_whom])
        encrypted = encryptor.encrypt(args.text)
        print("Encrypted:", binascii.hexlify(encrypted))
        
        ### SEND ENCRYPTED TEXT OVER EMAIL


    elif args.mode == 'recv':
        assert args.from_whom is not None, "sender's alias not provided. From whom is the inbound message?"
        print(f'fetching email from {my_email} now ...')

        ### FETCH EMAIL, EXTRACT PAYLOAD

        ### DECRYPT PAYLOAD

if __name__ == '__main__':
    main()
