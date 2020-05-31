#
 # import base64
 # def FileBase64Enc(path):
 #     with open(pat
 #             ,'rb') as image:#         FileEnc = image.read()
 #     FileEnc = base64.b64encode(FileEnc)
 #     return FileEnc;
 # def FileBase64Dec(s,save_path,name):
 #     s=base64.b64decode(s)
 #     with open(save_path+name, 'wb') as file:
 #         file.write(s)

#
# def CryptEn(s):
#     x = []
#     for i in range(len(s)):
#         j = ord(int(s[i])+2)
#         if j >= 33 and j <= 126:
#             x.append(str(chr(33 + ((((j)) + 14) % 94))))
#         else:
#             x.append(s[i])
#     return ''.join(x)
# def CryptDec(s):
#     x = []
#     for i in range(len(s),0):
#         j = ord(int(s[i])+2)
#         if j >= 33 and j <= 126:
#             x.append(str(chr(33 + ((((j)) + 14) % 94))))
#         else:
#             x.append(s[i])
#     return ''.join(x)
# def encryptoTop(s):
#     return str(rot47(str(base64.b64encode(bytes(rot47(s), encoding="utf8"))),iterations=150,salt="NotASalt"))
# def decryptoTop(s):
#     return str(rot47(str(base64.b64encode(bytes(rot47(s), encoding="utf8"))),iterations=150,salt="NotASalt"))
#
# import cr
# import base64
# from M2Crypto import RSA  # $ pip install m2crypto
#
# # ssh-keygen -f ~/.ssh/id_rsa.pub -e -m PKCS8 >id_rsa.pub.pem
# rsa = RSA.load_pub_key('id_rsa.pub.pem')     # load public key
# encrypted = rsa.public_encrypt(b'hello world', RSA.pkcs1_oaep_padding)  # encrypt
# print(base64.b64encode(encrypted).decode())  # print as base64
#
#
#
# from cryptography.fernet import Fernet
# key = b'' # Use one of the methods to get a key (it must be the same when decrypting)
# input_file = 'test.txt'
# output_file = 'test.encrypted'
#
# with open(input_file, 'rb') as f:
#     data = f.read()
#
# fernet = Fernet(key)
# encrypted = fernet.encrypt(data)
#
# with open(output_file, 'wb') as f:
#     f.write(encrypted)
#
#
# def rot47(s):
#     x = []
#     for i in xrange(len(s)):
#         j = ord(s[i])
#         if j >= 33 and j <= 126:
#             x.append(chr(33 + ((j + 14) % 94)))
#         else:
#             x.append(s[i])
#     return ''.join(x)
#
#
#
#
# from cryptography.fernet import Fernet
# def keyGen(password_provided):
#     import base64
#     import os
#     from cryptography.hazmat.backends import default_backend
#     from cryptography.hazmat.primitives import hashes
#     from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#
#     password_provided = "password"  # This is input in the form of a string
#     password = password_provided.encode()  # Convert to type bytes
#     salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=32,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
#     return key
#
#
# def EnCrypt(s):
#     s=s.encode()
#     key=keyGen("NotAPass")
#     f = Fernet(key)
#     encrypted = f.encrypt(s)
#     return (encrypted)
# def DeCrypt(s):
#     key=keyGen("NotAPass")
#     f = Fernet(key)
#     decrypted = f.decrypt(s)
#     return str(decrypted)
#
# print(DeCrypt(EnCrypt("q")))
#
# import base64
#
#
#
# def FileBase64Dec(s, save_path, name):
#     s = base64.b64decode(s)
#     with open(save_path + name, 'wb') as file:
#         file.write(s)
from cryptography import fernet

from cryptography.hazmat.primitives import kdf
import pbkdf2
key = b'HItG67RX3OME1ivpT56REHp257rpuvdyujKK-St6WI0='
f = fernet.Fernet(key)
def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)

def SuperFileDec(ss, save_path, name):
    import base64
    def FileBase64Dec(s, save_path, name):
        s = base64.b64decode(s)
        print(s)
        with open(save_path + name, 'wb') as file:
            file.write(s)

    def DeCrypt(s):
        decrypted = f.decrypt(s)
        return str(decrypted)

    return  FileBase64Dec(DeCrypt(ss),save_path,name)

def SuperFileEnc(path):
    import base64
    def EnCrypt(s):
        encrypted = f.encrypt(s)
        return (encrypted)

    def FileBase64Enc(path):
        with open(path, 'rb') as image:
            FileEnc = image.read()
        FileEnc = base64.b64encode(FileEnc)
        return FileEnc;

    return (EnCrypt(FileBase64Enc((path))))
print(SuperFileDec(SuperFileEnc('C:/Users/Valentin/PycharmProjects/NotADevs/NotACloud/NotAWeb/c.txt'),save_path="C:/Users/Valentin/PycharmProjects/NotADevs/NotACloud/NotAWeb/",name="cs.txt"))


