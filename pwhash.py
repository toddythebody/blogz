import hashlib
import random
import string

def makeSalt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

def makeHash(pw, salt=None):
    if not salt:
        salt = makeSalt()
    hash = hashlib.sha256(str.encode(pw + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)

def checkHash(pw, hash):
    salt = hash.split(',')[1]
    if makeHash(pw, salt) == hash:
        return True
    return False
