import base64, os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC



def encryptData(data, passwd):
    password = passwd.encode()  # Convert to type bytes
    salt = b'|\xd8\x99M\xc0C\xee->o\xf8\x90w\xd1\xc50'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    return encrypted


def decryptData(data, decryptKey):
    password_provided = decryptKey
    password = password_provided.encode()  # Convert to type bytes
    salt = b'|\xd8\x99M\xc0C\xee->o\xf8\x90w\xd1\xc50'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)
        return decrypted
    except InvalidToken as e:
        raise RuntimeError("Invalid Key")