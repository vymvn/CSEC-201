import string
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

from ChatBotServer import decryptMsg


key = b'8 bytes!'

# cipher = DES.new(key, DES.MODE_CBC)
# iv = cipher.iv
msg = b"My top secret message!!!!"


# encrypted = cipher.encrypt(pad(msg, DES.block_size))

# print(encrypted)


# deCipher = DES.new(key, DES.MODE_CBC, iv)

# decrypted = unpad(deCipher.decrypt(encrypted), DES.block_size)

# print(decrypted)

def encryptMsg(msg, key) -> bytes:
    cipher = DES.new(key, DES.MODE_CBC)
    iv = cipher.iv
    encryptedMsg = cipher.encrypt(pad(msg, DES.block_size))
    print(iv)
    return encryptedMsg, iv

def decryptMsg(encryptedMsg, key, iv) -> string:
    decryptionCipher = DES.new(key, DES.MODE_CBC, iv)
    decryptedMsg = unpad(decryptionCipher.decrypt(encryptedMsg), DES.block_size).decode()
    return decryptedMsg

encrypted, iv = encryptMsg(msg, key)
print(encrypted)
decrypted = decryptMsg(encrypted, key, iv)
print(decrypted)

# # encrypted = encryptMsg(msg, key)
# print(encrypted)
# cipher = DES.new(key, DES.MODE_OFB)
# decrypted = cipher.decrypt(encrypted)
# # decrypted = decryptMsg(encrypted, key)
# print(decrypted)