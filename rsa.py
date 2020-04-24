
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

def main():
    keyPair = RSA.generate(3072)
   
    f = open('mykey.pem','wb')
    f.write(keyPair.export_key('PEM'))
    f.close()

    f = open('mykey.pem','r')
    key = RSA.import_key(f.read())

    print(key.publickey().exportKey().decode('ascii'))
    print(key.exportKey().decode('ascii'))

if __name__ == '__main__':
    main()
