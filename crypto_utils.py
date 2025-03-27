
import base64
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

def pad(data):
    length = 16 - (len(data) % 16)
    return data + chr(length) * length

def unpad(data):
    length = ord(data[-1])
    return data[:-length]

def encrypt_aes(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(plaintext).encode("utf-8")
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(ciphertext).decode("utf-8")

def decrypt_aes(ciphertext_b64, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = base64.b64decode(ciphertext_b64)
    decrypted = cipher.decrypt(ciphertext).decode("utf-8")
    return unpad(decrypted)

def encrypt_rsa(plaintext, public_key_pem):
    public_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(plaintext.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def decrypt_rsa(ciphertext_b64, private_key_pem):
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(ciphertext_b64))
    return decrypted.decode("utf-8")
