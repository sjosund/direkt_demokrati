"""
Creates a secure hash and salt for storing of passwords. Uses 64bit SHA256 with a 64bit Salt
"""

import hashlib
import random
import string

def hash_pwd(password,use_salt=True):
    salt = ''
    if use_salt:
        salt += ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))

    hash_object = hashlib.sha256(password+salt)
    hex_dig = hash_object.hexdigest()

    return {'salt': salt, 'hash': hex_dig}

